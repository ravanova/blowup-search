# Leg 83 — LEG-J — Route-MFG v1 — adversarial audit of `marginal_flow.py`'s gate 11

**Date:** 2026-08-05/06. **Branch:** `leg/mfg-v1`. **Claim-bearing.** **Gate answer: NO.**

## Headline

Gate 11 flags **1 of 9** scored non-NaN divergent trajectories. The one it flags is the
finite-time blowup — the NaN case it was built for. **0 of 3** genuinely convergent controls is
falsely flagged. The worst miss grows the state by **4.99e130×** and ends at `mu = 1.50e130`
while its Newton residual/floor is **1.60e-02**, i.e. **1.6e-10 of the 1e8 threshold**.

Per the gate's `no` branch: `solver/marginal_flow.py` was **not** modified, and this branch is
**not** pushed to `main`. Escalated to the orchestrator.

## Order of work (the protocol, as executed)

1. `plan_of_record.py` run first. The gCLM-measurement ban (leg 42) was checked explicitly and
   recorded in the novelty log: this leg runs no sweep, computes no profile, and reads no new
   gCLM number — it pushes synthetic trajectories with closed-form solutions through the
   *existing* integrator's *existing* validity predicate. The "grep `capabilities.py` first" ban
   was also honoured; line 82–86 is the claim under audit.
2. **Novelty pass committed BEFORE construction** (`74b00f6`), `writeup/novelty/leg_83.md`.
   Four verbatim queries with links. It made a falsifiable prediction before any code existed:
   every clause of the predicate is an *inner-solve* observable while every published divergence
   detector is a *state* observable (SUNDIALS separates the two tests explicitly; the blow-up
   literature's detectors are all predicates on the solution), so smooth divergence with a
   healthy Newton would pass. The battery was then built to make that prediction falsifiable.
3. Construction, then measurement, then the note.

## What was built

* `experiments/p2_route_mfg_v1_adversarial.py` — 13-member battery. A `SyntheticFlow` duck-types
  `AugmentedFlow` so `integrate` runs on its **real code path** with a right-hand side whose
  exact solution is known in closed form.
* `writeup/data/p2_route_mfg_v1_adversarial.json` — curated data, all magnitudes per member.
* `test_marginal_flow_adversarial.py` — permanent regression test, 8 gates, **6 s**.
* Findings note appended to `writeup/novelty/leg_83.md`.

## Two decisions worth keeping

**A fidelity gate, and it bound on a real case.** A divergent member counts only if the
*computed* trajectory is verified to still diverge. `osc_stiff_underresolved` (`omega dt = 4`
rad/step) was damped by BDF2's L-stability to **3.5e-14** of its exact amplitude — so the
trajectory the predicate saw genuinely converged, and scoring it as a miss would have blamed the
gate for the integrator. It is excluded from the statistic (dropping the count from a flattering
9/10 to an honest 8/9) and reported as a **separate hazard**: an under-resolved sustained
oscillation is silently turned into a spurious decay, with `converged = True` and every
diagnostic healthy, and no `dt`-vs-`max|Im|` guard exists to catch it.

**Live controls before new verdicts.** The two trajectories inside gate 11 itself were re-run on
the real `AugmentedFlow` at K = 96 and both reproduce its verdicts (trap → `False` at
residual/floor 1.28e13; on-branch → `True` at 6.28e2). Without that, a "miss" could have been the
synthetic harness misbehaving.

## Mechanism, asserted rather than inferred

`test_8` puts the exact fixed point and a state **1.2e13×** larger side by side: they agree on
all three clauses. No state clause can exist. `osc_sustained` makes the same point from the other
direction — amplitude **1 forever**, nothing large anywhere, still missed — which is why the
finding is *"the predicate does not look at the state"* and not *"the threshold is too high"*.

## Severity

`rec["converged"]` has one consumer: `p2_route_i_v1_driven.py::i4_adiabaticity`. **No banked
number is shown to be wrong** — the three accepted off-branch runs in
`writeup/data/p2_route_i_v1_driven.json` agree with the on-branch reference to 1.4e-10, 4.0e-10
and 4.3e-10 relative, with `alpha_1` matching to ten significant figures. But that protection is
the *driver's own redundant comparison*, not the gate. A smoothly divergent run would have been
accepted and its `alpha_1` quoted.

## Territory

Diff touches only: `test_marginal_flow_adversarial.py`,
`experiments/p2_route_mfg_v1_adversarial.py`, `writeup/data/p2_route_mfg_v1_adversarial.json`,
`writeup/novelty/leg_83.md`, `experiments/journal/leg_83.md`. `solver/marginal_flow.py` read
only. No shared ledger touched.

## For the orchestrator

Disposition is in the note's last section: narrow `capabilities.py`'s validated line; add a state
clause (the quantities are already in `rec` and simply unused); add a `dt`-vs-`max|Im|` guard for
Finding 3. **None of it executed here** — the gate's `no` branch forbids patching under this
leg's authority. The regression test's characterization assertions will START FAILING when a
repair lands; flip them, never weaken them.
