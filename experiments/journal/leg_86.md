# Leg 86 — Route-PCB v1: the post-repair regression check of the line-sweep preconditioner

**Date: 2026-08-06. Kind: regression check — light. No figure. No new physics, and none claimed.**

## Gate, verbatim

> After the bench-repair, does `solver/port_certification.py`'s line-sweep preconditioner still
> (a) hit the 9.5e-16 precision gate it was originally validated to, and (b) run within normal
> benchmark variance of its pre-repair timing?

## Answer

**YES, on both halves, and the strongest available form of yes on (a).**

- **(a) precision.** The configuration the 9.5e-16 was measured on — `test_7`'s seed 11, 48×16,
  drho 0.09, dbeta 0.033, c −1.0145 — returns the full transport operator's own right-hand side
  to **9.4723e-16**, i.e. **1.00×** the advertised figure, and it returns it to *that same value*
  before and after the repair. Across a 20-configuration battery (grids 48×16 → 300×48, the
  marginal-`s_rho` regime at `s_rho ∈ [1e-3, 5e-3]`, both field scalings), the sweep's output is
  **bit-for-bit identical** to the pre-repair module's: **20/20 cases, 0 of 131 136 entries
  differing, worst ULP gap 0**. Not "both are small" — *nothing moved*.
- **(b) timing.** Interleaved pre / post / **post-null** rounds (15 rounds × 6 calls, two grids).
  Median deviation **+0.21%** at 300×48 (24.33 → 24.38 ms) and **+1.12%** at 96×32 (5.76 → 5.83
  ms), against a **null arm** — post-repair timed against post-repair, same round, same machine —
  of **0.29%** and **0.20%**. Worst deviation 1.12%, budget max(3× null, 10%) = 10%. The
  deviation is also **sign-inconsistent** across the two grids in a first (loaded-machine) run
  and sub-percent in the clean one, which is the signature of scheduler noise rather than a cost.
- **Corroboration from the source side.** The repair commit (`3f187d8`) is **+58/−0 lines** across
  exactly two top-level definitions, `_hypothesis_violations` and `radii_polynomial_status`.
  **Zero** of them are on the sweep's call path (`line_sweep_solve`) or the adjacent hot path
  (`make_preconditioner`, `leading_order_solve`, `gmres`, `krylov_ladder`). The repair was
  textually surgical, and the numbers agree.
- **Consequence arm.** A preconditioned Krylov ladder built on the sweep (300×48, perturbed
  transport operator, m = 10…80) gives **3.603020e-14 at m = 80 in both versions, all 4 rungs
  identical**.

**The repair was surgical. Banked as a permanent regression test.**

## Secondary finding, reported not patched: the 9.5e-16 figure is per-configuration, not uniform

The battery's **worst** relative residual is **1.008e-14 — 10.61× the advertised 9.5e-16** — on
the 300×48 grids. This is **not a regression**: it is **exactly equal** pre- and post-repair
(that equality is asserted in the artifact and in gate 5 of the test file), and it is what an
O(N) sweep does when N grows. It is a caveat on how `capabilities.py` line 107 words the claim —
"line sweep gated to 9.5e-16 against the operator it inverts" reads as uniform and is measured on
one 48×16 configuration.

`capabilities.py` is **outside this leg's territory and was not touched**. Flagged here for
whichever leg owns that file: the accurate wording is "9.5e-16 on `test_7`'s configuration; 1.0e-14
worst over 48×16…300×48", and the honest tightening of `test_port_certification.py`'s `test_7` is
from `err < 1e-11` to the advertised number — a ~4-decade gap that this leg's gate 1 now covers
from a separate file rather than by editing someone else's.

## What was done, in order

1. `plan_of_record.py` run first, every ban read. None tripped (see `writeup/novelty/leg_86.md`
   §3): no gCLM measurement, no Route-D sharpening, no DSS re-ask, no GA compute, nothing
   re-opened.
2. `capabilities.py` grepped before construction; the `solver/port_certification.py` entry
   (lines 103–118) read in full **as rewritten by leg 79's repair**, which is where the 9.5e-16
   and the 11/25 → 0/25 both come from.
3. Novelty pass run and **committed before construction** (`09b7de9`). It found the one thing
   that mattered: `test_7` asserts `err < 1e-11` against a 9.5e-16 claim, so the existing gate
   could not have caught a four-decade regression. It also pre-committed the two methodological
   choices below, **before any number was seen**.
4. Two pre-commitments, honoured: the precision arm is **bit-for-bit**, not "both are small"; the
   timing arm carries a **null**, because "within normal benchmark variance" is unanswerable
   unless the variance is measured in the same run. `test_route_g_perf.py`'s doc-string already
   refuses "a timing anecdote"; a bare pre/post ratio would have been one.
5. `experiments/p2_route_pcb_v1_postrepair.py` recovers the pre-repair module from
   `git show <repair>^:solver/port_certification.py` — the commit located **by subject line**,
   not by hash, so a rebase cannot silently break it — imports it beside the working-tree module,
   and runs P1 (static) / P2 (precision) / P3 (timing) / P4 (consequence) on both.
6. `test_port_certification_postrepair.py`: 5 gates, ~2 s, all pass. Gate 1 holds the canonical
   configuration to the **advertised** number rather than to `test_7`'s loose one; gate 2 is the
   bit-for-bit comparison; gate 3 is the static disjointness; gate 4 is the timing arm with a
   4×-null budget (wider than the bench, because CI is noisier — the null adapts); gate 5 pins
   the artifact *and* pins the scope caveat as pre-existing so it can never be re-read as damage.

## `solver/port_certification.py` was read and never edited, under either gate outcome.

## Data

`writeup/data/p2_route_pcb_v1_postrepair.json` — the four clauses, all 20 precision rows with
their pre/post pairs and ULP gaps, both timing grids with all three arms, and the gate answer
assembled from magnitudes.
