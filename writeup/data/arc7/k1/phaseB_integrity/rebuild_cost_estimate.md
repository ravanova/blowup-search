# What a SEMANTIC-MATCH check would cost — measured on the phase-B container, 2026-09-10

Phase B's GREEN and the comparator PASS (`integrity.json`) leave one limit open: **do mathlib's
cached oleans mean what mathlib's source text says?** Only recompiling from source answers that.
This file measures the price of two ways to do it. It is a cost measurement, not a check: nothing
here verifies anything, and no reading changes.

## Method
`lake env lean <file> -o <scratch>` on random mathlib modules from phase B's tree, timed. Two
disjoint samples, seeded (`shuf --random-source`), scratch output outside the repo, tree untouched.
- Sample A, n=40, **sequential** → per-file cost.
- Sample B, n=40 (disjoint), **4-way parallel** → real speedup on these 4 cores.

A first attempt ran 64 files 4-way with a cold page cache and reported a mean of 28 s/file. It was
wrong: `Mathlib/Topology/Algebra/InfiniteSum/Constructions.lean` reported 340 s there and takes
13 s alone. Contention plus cold cache, not cost. Recorded here so the discarded number is not
rediscovered and believed.

## Measurements
| Quantity | Value |
|---|---|
| Sample A mean | 3.81 s/file (sd 3.19, 95% CI of the mean 2.82–4.80) |
| Sample A median / p90 / max | 2.6 s / 8.8 s / 15.7 s |
| Sample B speedup, 4 cores | 3.30× |
| mathlib, all 8370 files | 8.9 CPU-hours; **≈2.7 h wall** on 4 cores (CI 2.0–3.4 h) |
| project's own 2484 modules | 5443 s = 1.5 h wall (measured in phase B, not extrapolated) |
| **full from-source build, everything** | **≈4 h wall on 4 cores** |
| **targeted: 399 modules (below)** | **≈25 CPU-min; ≈8–10 min wall on 4 cores** |

Anchor: phase B's real `lake build` did 2484 project modules at 2.19 s/module wall on these cores.

Not modelled: lake's per-module extras (`.ilean`, `.ir`) and mathlib's own `leanOptions`, which the
single-file sample skips. Both are small beside elaboration, but they push the estimate up, not down.

## The targeted alternative, and why it is smaller
Proof bodies are already kernel-checked twice (Lean's kernel and nanoda, `integrity.json`), so a
wrong olean for some lemma's *proof* cannot pass. What is unchecked is **meaning**: the definitions
appearing in the two theorem *statements*. `statement_closure.lean` computes that closure — the type
of every constant, the *value* of every definition, and the *constructors* of every inductive, with
theorem proof bodies deliberately not followed. Output in `statement_closure.txt`:

```
statement_closure_constants = 5579
MATHLIB modules in statement closure = 399   (of 8370)
```

It contains the machinery the statement should rest on: `Analysis.Calculus.FDeriv.Defs`,
`ContDiff.Defs`, `Deriv.Basic`, `InnerProductSpace.Laplacian`, `InnerProductSpace.PiL2`.

**Comparison must be at declaration level, not bytes.** Rebuilt oleans are not byte-identical to
cached ones (build flags and the module-system `.olean`/`.olean.private`/`.olean.server` split); a
spot check found ~1% size differences on files that compile fine. Use `lean4export` on both
environments and diff the declarations in the closure.

**What the targeted check would and would not establish.** It would establish that those 399 modules
elaborate from source to the declarations the cached oleans hold. It assumes the surrounding
environment used during that elaboration is faithful. The full rebuild removes that assumption; the
targeted one does not, and must be written up saying so.

## Blocker for the full version, measured
`/root` had 11 GB free; mathlib's build output alone is 6.6 GB. A second tree does not fit without
freeing space, and phase B's tree is both the evidence and what K2 needs, so it must not be reused
or deleted. The targeted check has no such problem: it writes a few hundred oleans to scratch.
