# Leg 437 — unit `K1`, arc 7: THE KERNEL CHECK — pre-registration, pushed BEFORE the run

**Date:** 2026-09-10. **Role:** SERIAL, Conductor-run. **Charter:** the user's arc-7 charter, item K1,
recorded at `CORRECTIONS.md` §72. **Runner:** `scripts/arc7_k1_kernel_check.sh`. **Time cap: NONE.**
The build runs in the background, checkpoints progress in its own log, and is never killed to stay
inside a wall-clock guess.

## §1. The gate, in the charter's words — four answers, separately
(a) does `lake exe cache get && lake build` run **to completion** (exit 0, zero `error:` lines, every
default target — `NavierStokes`, `Euler`, `ComparatorChallenges` — built);
(b) `#print axioms` output **verbatim** for `NavierStokes.Comparator.navier_stokes_breakdown_R3` and
`NavierStokes.Comparator.navier_stokes_breakdown_periodic`;
(c) is `sorryAx` reachable from either — **YES / NO**;
(d) wall time and machine (toolchain, mathlib rev, cores, RAM, CPU model), so a reader can reproduce it.

## §2. Pre-committed readings
- **GREEN:** (b) is `[propext, Classical.choice, Quot.sound]` and nothing else, for both theorems, and
  (a) completes. Then: **STOP AND REPORT.** No extension, no generalisation, no claim about Theorem 1.1.
- **RED:** `sorryAx` present, or any axiom outside the standard three, reachable from either theorem.
  Then: **STOP AND ESCALATE. NO PUBLICATION. NO COMMITTED CLAIM.** Packet in `writeup/escalations/`,
  naming the declaration and the axiom; then a blind agent reproduces it from the same commit before
  anyone says a word.
- **INCOMPLETE:** the build does not complete (network denial, disk, crash). Then (a) is
  `NOT-ESTABLISHED` with the blocker named and measured; (b)–(c) are answered only if the
  `ComparatorSolution` olean exists, and are labelled as answered on a partial build.

## §3. Two phases, both pre-committed, in this order — and why
The arc-6 tree at `8937a8f4` survived in the previous session's scratchpad: `NavierStokes` fully built,
`Euler` stopped at `[10526/11251]` when leg 435's session ended, mathlib oleans from the official cache.
Disk in this container (8.8 GB free) holds one tree, not two.
- **Phase A — resume that tree to completion.** `lake build` continues where it stopped (725 jobs, all
  `Euler`), then `#print axioms`. Cheap, and it answers (a) even if the cache host is denied again
  (leg 418's failure mode). Its wall time is **partial** — the NavierStokes part was built in leg 435 —
  and is recorded as such, never as the reproduction figure.
- **Phase B — a fresh clone at the same pinned commit, `lake exe cache get`, `lake build` from nothing,
  timed end to end, then `#print axioms`.** This is the reproduction figure for (d). Phase A's tree is
  deleted only after its artefacts are banked, to make room.
The two phases are the same command sequence on the same commit, in the same container, by the same
Conductor: **phase B is a second run, not a second agent.** `UNVERIFIED` until a blind agent reproduces
it (§3f rule 1); K2 slot 2 cross-checks its axiom output against the source census.

## §4. What a GREEN result does and does not establish (written before the number)
It establishes that the Lean 4 kernel (v4.34.0-rc2) accepted two theorems whose proofs use only
mathlib's standard three axioms, on this machine, at this commit. Those theorems are Fefferman (C)/(D)
as the project formalises them — strictly weaker than the paper's Theorem 1.1 (leg 431 gate (b)).
It does not establish Theorem 1.1, that the Lean proof follows the paper's argument, that mathlib's
cached oleans match their sources, or anything about priority. It is a machine check, not a referee.
