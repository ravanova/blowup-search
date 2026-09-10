# Leg 437 phase C — unit `K1`, arc 7: THE FROM-SOURCE REBUILD — pre-registration, fixed BEFORE anything builds

**Date:** 2026-09-10. **Role:** SERIAL, operator-run on the user's laptop. **Branch:**
`leg/437-k1-phaseC-from-source`. **Parent pre-registrations:** `leg_437_prereg.md` (gate (a)–(d),
readings), `leg_437_prereg_amend.md` (phase B relocation). **Time cap: NONE.** The build runs in the
background and is never killed to fit a wall-clock guess (leg 431 §3 item 1).
**The leg number is the Conductor's to assign; the branch name is kept and the leg renumbered.**

## §1. Why this run exists — the limit it closes
Every K1 run so far (phase A, phase B, phase B local) replayed mathlib's compiled `.olean` files from
the official cache. Two kernels accepting those oleans establishes that their **contents** are
kernel-valid. It does **not** establish that they **mean what mathlib's source text says**: the cache
sits in the trust path. Phase C compiles mathlib **from source**, so the cache is not in the trust
path at all. This is the last of the three limits banked against K1
(`writeup/data/arc7/k1/phaseB_integrity/rebuild_cost_estimate.md`).

## §2. Pre-committed readings — fixed before anything builds
- **MATCH** — build rc 0, **and** `#print axioms` on
  `NavierStokes.Comparator.navier_stokes_breakdown_R3` and
  `NavierStokes.Comparator.navier_stokes_breakdown_periodic` is **exactly**
  `[propext, Classical.choice, Quot.sound]`, identical to `phaseB.json`'s `axioms_verbatim`.
  **Conclusion: the cached oleans were not load-bearing.**
- **MISMATCH** — any difference in the axiom lists, or a build error the cached build did not have.
  **STOP. Do not push a claim anywhere.** Bank the logs, write `writeup/escalations/`, name the
  declaration and the difference **verbatim**.
- **INCOMPLETE** — disk, crash, or toolchain failure. Bank the blocker **measured**, with the number.

## §3. Precondition, measured, ABORT IF IT FAILS
Record `nproc`, CPU model, `free -g`, `df -h $HOME`. The run needs **roughly 20 GB free**: mathlib's
build output alone measured **6.6 GB**, and from source the tree also carries `.ir` and `.ilean` for
~8370 modules plus the project's 2486 oleans. **If 20 GB free cannot be shown, the run does not
start:** bank INCOMPLETE with the measured number and stop. (Phase B local started with 11 GB free and
survived only because the cache `.ltar` files were parked in `/dev/shm`; from source there are no
`.ltar` files to park — the space is the build output itself, which must live in the tree.)

## §4. The run, if the precondition holds
Fresh clone of `https://github.com/openai/NavierStokesAndEuler.git` into a work tree **outside this
repository**; checkout `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`; confirm `lean-toolchain` reads
`leanprover/lean4:v4.34.0-rc2`. Then, and this is the whole point:

> **DO NOT RUN `lake exe cache get`. NOT ONCE.** Not to "warm" anything.

`lake build` alone, background, no time cap, logging to
`writeup/data/arc7/k1/phaseC/k1_C_build.log`. Expect 2–4 h on 12 cores (mathlib measured at 8.9
CPU-hours). **Proof that the cache was not used:** `grep -c "Built Mathlib\."` on the log must be in
the **thousands**. If it is 0, a cache was used and **the run is void**.

## §5. The checks, in the built tree
- **(a)** `#print axioms` on both theorems, exactly as `scripts/arc7_k1_kernel_check.sh` does it,
  output **verbatim** to `k1_C_axioms.log`.
- **(b)** `mathlib_rev` (expect `85e3a25e006c35636f0e53b0e9296caca2685bc0`), Comparator rev (expect
  `19e111e2141cf333c7daff0f64c5f24acc91dd2e`), the final `[n/N]` (expect 11251 jobs), error line
  count, olean count.
- **(c)** the comparator on `ComparatorChallenges/NavierStokes.json` and `Euler.json` under a **real**
  landrun built from source, as K2 slot 3 did. If landrun will not build here, **say so and skip it**
  rather than substituting the fake shim; the shim's deviation is closed elsewhere and is not repeated.

## §6. What a MATCH would and would not establish (written before the number)
It would establish that the two theorems' axiom lists are unchanged when mathlib is compiled from its
own source on this machine, at this commit — i.e. that the cached oleans were not load-bearing for
this result. It would **not** establish the paper's **Theorem 1.1**: the two statements are Fefferman
**(C)/(D)** as the project formalises them (leg 431 gate (b)), strictly weaker. It is a **machine
kernel check of two statements**, not a proof of Theorem 1.1, and must never be described as one.
It also would not establish verification by a **second agent** (§3f rule 1) — same Conductor's brief.

---
*Added at bank time, after the §3 precondition was measured:* the outcome of this pre-registration is
banked in `writeup/data/arc7/k1/phaseC/phaseC.json`. The readings above were fixed before any
measurement was taken.
