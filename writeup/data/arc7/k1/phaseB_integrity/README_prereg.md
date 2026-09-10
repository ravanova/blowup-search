# Leg 437 — K1 phase B follow-on: INTEGRITY + PROVENANCE of the cached mathlib oleans, WITHOUT recompiling mathlib

**Date:** 2026-09-10, after phase B banked GREEN (`../phaseB/phaseB.json`). **By user direction in the
phase-B session** ("do what we can without running the whole thing again"), not a pre-registered K1 phase;
it is the K2 slot-3 comparator step run early, on phase B's tree, by the same session. Written and pushed
BEFORE the comparator ran.

## The question, split three ways
"Do the mathlib oleans match?" is three claims:
1. **Provenance** — the oleans are the ones mathlib CI built from these sources. Re-verified from the
   traces and cache hashes (`provenance.log`); it establishes labelling, not compilation.
2. **Integrity** — every declaration in the solution environment (the full import closure, mathlib
   included) is kernel-valid and uses no axiom outside the permitted three. Checked here by
   `lake exe comparator` (leanprover/comparator @ `19e111e2`): `lean4export` of the solution environment,
   statement identity against the challenge module, axiom check, replay through the Lean kernel, and
   replay through **nanoda** (an independent Rust kernel) — the project's own verification recipe
   (`ComparatorChallenges/README.md`).
3. **Semantic match** — the oleans mean what the source text says. NOT checked here; only a recompile
   of the closure does that, and the closure is all 8371 mathlib modules (project files import `Mathlib`).

## Pre-committed readings for (2)
- **PASS:** comparator exits 0 on `ComparatorChallenges/NavierStokes.json` (both K1 theorems), with the
  builtin kernel replay and the nanoda replay both reported successful. Euler is run as well and
  reported separately; it is not part of the K1 gate.
- **FAIL:** comparator exits non-zero for a reason inside the check (statement mismatch, forbidden
  axiom, kernel rejection by either kernel). Then: STOP, bank verbatim, escalate, no claim.
- **INCOMPLETE:** the run does not finish (crash, memory, disk, tool failure outside the check). Bank
  the blocker measured.

## Deviations from the full comparator recipe, declared up front
- `landrun` (the sandbox) is replaced by the comparator's own `scripts/fake-landrun.sh` shim: building
  landrun was blocked by this session's permission policy. The sandbox exists to contain an
  adversarial `Solution.lean` during compilation; here the tree is fully prebuilt (phase B), so the
  comparator recompiles nothing — the README's own "fully pre-built `.lake` directory" case.
- No `systemd-run` wrapper, for the same reason.
- Same Conductor-directed session as phase B: a second machine and a second kernel, not a second agent.

## What a PASS does not establish
Claim 3 above; Theorem 1.1 of the paper (the statements are Fefferman (C)/(D)); anything about priority.
