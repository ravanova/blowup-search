# Leg 437 phase C — ADDENDUM to `leg_437_phaseC_prereg.md`, written BEFORE the run starts

**Date:** 2026-09-11. **Branch:** `leg/437-k1-phaseC-from-source`. **Supersedes:** nothing. The
readings of `leg_437_phaseC_prereg.md` §2 (MATCH / MISMATCH / INCOMPLETE) are **unchanged**, as is the
§4 rule that `lake exe cache get` is never run and the §4 void condition (`Built Mathlib.` count of 0).

## What changed: the §3 precondition, re-measured, now PASSES
The first attempt on 2026-09-10 banked **INCOMPLETE** (`writeup/data/arc7/k1/phaseC/phaseC.json`):
3474485248 bytes (3.24 GiB) available against the ~20 GB required. On the operator's instruction disk
space was then freed on the machine. Re-measured immediately before this run:

```
available to a build (statvfs f_bavail)   21.5 GB  = 20.06 GiB
physically free       (statvfs f_bfree)   33.9 GB  = 31.56 GiB
```

The pre-registered requirement is "roughly 20 GB". It is **met, but with little margin** — that fact is
recorded here in advance rather than discovered in a post-hoc explanation. If the build exhausts the
disk, the reading is **INCOMPLETE** with the measured blocker, exactly as §2 already provides; it is
**not** a MISMATCH, and no axiom claim follows from it.

## Provenance of the freed space, for a reader asking whether the tree is clean
The space came from removing merged git worktrees and regenerable package caches on the operator's
machine. **Nothing in the Lean trust path was touched**: no mathlib source, no olean, no cache
archive, no toolchain. The toolchain `leanprover/lean4:v4.34.0-rc2` was already installed before the
first attempt and is unchanged.

## What this addendum does not change
The gate, the readings, the pin `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`, the prohibition on
`lake exe cache get`, and the scope statement: this is a **machine kernel check of two statements**
that are Fefferman **(C)/(D)** as the project formalises them, **not** a proof of Theorem 1.1.

**Deviation class:** a pre-registration whose measured precondition changed state between attempts,
re-measured and recorded before the run it governs — not a widening, not a retry after seeing a result.
