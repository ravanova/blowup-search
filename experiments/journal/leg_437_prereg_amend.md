# Leg 437 — AMENDMENT to `leg_437_prereg.md` §3, BY USER RULING 2026-09-10, BEFORE PHASE B RAN

**What changes:** phase B — the fresh clone at the pin, `lake exe cache get`, `lake build` from nothing,
timed end to end, then `#print axioms` — is **relocated to a fresh container** (a new Claude Code Remote
session in this environment, `source_revision` = the branch carrying the runner and this amendment)
instead of running in this container after deleting phase A's tree. **Phase A's tree is kept** for K2
slot 3 (the comparator steps: `lean4export` + `nanoda`) and slot 5.

**Why (the user's question and the Conductor's assessment, recorded):** phase B changes none of gates
(a)–(c), which phase A answered GREEN; it exists for (d), an end-to-end time on a clean tree, and for the
provenance argument that nothing survived from the interrupted arc-6 builds. Running it here would cost
K2 the built tree (disk holds one) for a same-container figure. A different container gives (d) on a
clean machine **and** adds the one thing the prereg's same-container design lacked: a second
environment. It re-tests the reproduction recipe from nothing (leg 418's cache-host failure mode).

**What it does not change:** the pre-committed readings (GREEN / RED / INCOMPLETE) apply unchanged to
phase B's output; the runner `scripts/arc7_k1_kernel_check.sh B` is unchanged; the gate wording is
unchanged. **Phase B in a fresh container is a second machine, not a second agent:** it is directed by
the same Conductor and stays `UNVERIFIED` under §3f rule 1 until a blind agent reproduces the axiom
output from the same commit (K2 slot 2 cross-checks against the source census).

**Where phase B's artefacts land:** `writeup/data/arc7/k1/phaseB/` (`phaseB.json` in the phase-A schema,
`k1_B_summary.txt`, `k1_B_build.log`, `k1_B_axioms.log`, the machine block from the fresh container),
committed by the fresh session on branch `leg/437-k1-phaseB` and pushed there — **never merged to
`main` by that session**; the Conductor integrates after reading the log, and a RED result stops
everything per prereg §2.

**Deviation class:** a pre-registration amended before the run it governs, on the user's ruling, with
the reason beside it — not a widening, not a skipped phase. `CORRECTIONS.md` §73.
