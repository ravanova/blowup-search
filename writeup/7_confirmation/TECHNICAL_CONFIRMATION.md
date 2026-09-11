# Arc 7 — Confirmation: running the Lean kernel to completion, and what that does and does not settle

**Legs 436–440 (`K0`–`K4`), 2026-09-10, `ORCHESTRATION.md` §3g CONDUCTOR, wave sizing 5.**
Every number below is cited **by JSON field** under `writeup/data/arc7/`. Re-derive them from the files,
not from this page: `.venv/bin/python writeup/7_confirmation/confirmation_evidence.py`.

---

## 0. The verdict, first — pre-registered in `leg_440_prereg.md` §2 before this page existed

> **The Lean kernel check is GREEN and VERIFIED: on one pinned commit, in three environments and by two
> independent kernels, both exported theorems are accepted depending on no axiom beyond `propext`,
> `Classical.choice` and `Quot.sound`, with `sorryAx` unreachable. That is the whole of what arc 7
> confirms. It confirms that the Lean project proves what its own statements say — and those statements
> are Fefferman's alternatives (C)/(D), which are strictly weaker than the manuscript's Theorem 1.1. It
> is not a confirmation that the 166-page proof is correct, and this repository's independent attempt to
> check the construction numerically produced ZERO surviving evidence in either direction.**

Everything below qualifies that paragraph. Nothing below replaces it.

**Addendum, 2026-09-11 — the verdict above is left VERBATIM; this is written beside it.** The verdict
was pre-registered before this page existed and says "three environments". There is now a **fourth**
run, and it closes the first of the three banked limits: mathlib has been **rebuilt from its own
source**, with the official olean cache never consulted, and both theorems return the same three axioms
byte for byte (§3b, `writeup/data/arc7/k1/phaseC/`). The verdict's substance is unchanged — what changes
is that it no longer rests on cached oleans.

**On authorship: this repository takes no position whatsoever on the priority dispute around the
manuscript.** Not a hedged position, not an implied one. It is outside what any measurement here can
reach, and no sentence in arc 7 should be read as leaning either way.

---

## 1. What arc 7 was asked (`K0`, leg 436)

The user's ruling of 2026-09-10 (`CORRECTIONS.md` §72): the programme is **not** finished, and its new
goal is to *independently **confirm** the OpenAI Navier–Stokes result — not re-derive it — by running the
Lean kernel to completion on its exported theorems, because out-refereeing 166 pages is beyond this
repository and running a kernel is not, and nobody has published a kernel run.*

`K0` recorded the rulings and corrected two discrepancies between the charter and the board, including
re-describing arc 6's kernel check as what it actually was: `#print axioms` on a build that **never
completed** (Euler 725 jobs short, mathlib from cache). Rulings 5 and 6 remain **unruled**, awaiting the
user; nothing in arc 7 depends on them.

## 2. `K1` (leg 437) — the kernel check, GREEN in three environments

Runner `scripts/arc7_k1_kernel_check.sh`. Pin `tree_head` = `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`,
`mathlib_rev` = `85e3a25e006c35636f0e53b0e9296caca2685bc0`, `comparator_rev` =
`19e111e2141cf333c7daff0f64c5f24acc91dd2e`, `toolchain` = `leanprover/lean4:v4.34.0-rc2`,
`olean_count` = 2486 — identical across all three.

| | artefact | `build_rc` | `build_error_lines` | timing | machine |
|---|---|---|---|---|---|
| **A** resume, remote container 1 | `k1/phaseA/phaseA.json` | 0 | 0 | `build_s` 2047 | 4 × Xeon 2.80 GHz, 15 GB |
| **B** fresh clone, remote container 2 | `k1/phaseB/phaseB.json` | 0 | 0 | `total_s` **5605** (`clone_s` 2, `cache_get_s` 121, `build_s` 5443, `axioms_s` 8) | 4 × Xeon 2.10 GHz, 15 GB |
| **B-local** fresh clone, the operator's laptop | `k1/phaseB_local/phaseB.json` | 0 | 0 | `total_s` **4272** (`clone_s` 2, `cache_get_s` 117, `build_s` 4148, `axioms_s` 5) | 12 × i7-10750H 2.60 GHz, 31 GB |

`Build completed successfully (11251 jobs).` in every one. In all three, `axioms_verbatim` reads

    'NavierStokes.Comparator.navier_stokes_breakdown_R3' depends on axioms: [propext, Classical.choice, Quot.sound]

and the same for `…_periodic`. **`sorryAx` reachable: NO**, everywhere.

**The gate's pre-committed reading (`leg_437_prereg.md` §2): GREEN in every environment → STOP AND
REPORT.** No extension, no generalisation, no claim about Theorem 1.1. That is what was done.

## 3. `K1`'s three banked limits — ONE NOW CLOSED (2026-09-11), the other two standing, neither softened

1. ~~**mathlib's oleans were REPLAYED from the official cache, not rebuilt from source.**~~ **CLOSED
   2026-09-11 by phase C — see §3b.** mathlib has now been compiled from its own source, with the cache
   never consulted, and the axioms are byte-identical. Struck, not deleted: it was a real limit for the
   three runs above, and every artefact banked under those runs still carries it.
2. **The statements are Fefferman's (C)/(D), not the manuscript's Theorem 1.1** — strictly weaker, with
   five existence clauses absent.
3. **A second machine is not a second agent.** Three runs by one lineage is not verification (§3f rule 1:
   *verification is a fresh session or it is not verification*).

### 3a. Limit 1 was two claims; this closed the first (2026-09-10, `k1/phaseB_integrity/`) — the second closed the next day, §3b

- **PROVENANCE — established to labelling only.** mathlib's cache is content-addressed; 8747 `.ltar`
  files, 442 MB, every recomputed key matching a file already present (`second_cache_get` rc 0 in 14 s,
  *No files to download*), and `second_lake_build` rc 0 in 11 s with **0 `Built` lines, 4 `Replayed`**.
  `provenance.what_this_does_not_establish`, verbatim: *that the labelled bytes were in fact produced by
  compiling those sources* — the trust sits with mathlib's CI and the cache host.
- **INTEGRITY — ESTABLISHED, by two independent kernels.** `lake exe comparator`:
  `integrity.navier_stokes.rc` = 0 in 913 s, `integrity.euler.rc` = 0 in 1442 s, `integrity.total_s`
  2355. Both report `lean_kernel` = **accepts** and `nanoda` = **accepts** — nanoda 0.4.17
  (`ammkrn/nanoda_lib @ 4c544ed4`), an **independent Rust implementation of the Lean kernel** — with
  statements identical to the challenge modules and nothing recompiled. Verdict string:
  `Your solution is okay!` Euler was run for completeness and is **not** part of the `K1` gate.
- **SEMANTIC MATCH — ESTABLISHED 2026-09-11, by the full rebuild, not the targeted alternative.**
  This bullet previously read *NOT established*, costed at ~4 h and blocked on disk. The user scheduled
  it; it ran; see §3b. The targeted 399-module check was **never needed and was not run** — the full
  rebuild subsumes it.

### 3b. Limit 1 is now CLOSED: mathlib rebuilt FROM SOURCE, 2026-09-11 (`k1/phaseC/`)

Pre-registered in `leg_437_phaseC_prereg.md` with `MATCH`/`MISMATCH`/`INCOMPLETE` fixed and pushed
**before** the run. A fresh clone at the same pin `8937a8f4`, outside the repository, then `lake build`
alone — **`lake exe cache get` was never invoked, not once.** The string `cache` does not occur anywhere
in the 732 KB build log.

The pre-registration's own void condition decides whether the run counts: if `Built Mathlib.` is 0, a
cache was used and the run is void.

| | phase C | phase B (laptop) | phase B (container) |
|---|---|---|---|
| `Built Mathlib.` lines | **8370** | 0 | 0 |
| `Replayed Mathlib.` lines | **0** | — | — |
| mathlib's origin | **compiled here, from source** | official cache | 8747 `.ltar` downloaded |
| wall time, end to end | **11578 s** | 4272 s | 5605 s |

**Reading: `MATCH`.** `lake build` rc 0, 0 error lines, `Build completed successfully (11259 jobs)`, and
both theorems report `[propext, Classical.choice, Quot.sound]` — compared **as bytes, not by eye**: the
`depends on axioms` lines from phase C, phase B (laptop) and phase B (container) all hash to
`0883b714ddd5c08564bf58dbb22edf44`, and `diff` is empty in both pairings. `sorryAx` does not appear.
Per the pre-registration this reads: **the cached oleans were not load-bearing.**

The price of removing the cache from the trust path, same laptop both times: **2.71×** wall clock
(11578 s from source against 4272 s cached) and a **28.5 GB** build tree.

Under `leg_437_phaseC_prereg.md` §5(c) the comparator was also re-run against this from-source tree under
a **real `landrun` built from source** (v0.1.17) — the declared shim of the earlier follow-on was *not*
substituted. **Lean's default kernel accepts both** challenge solutions. The nanoda leg did **not** run:
`nanoda_bin` is absent and uninstallable on that machine, so the comparator's *"nanoda kernel rejected"*
is its own phrasing for an `exec` failure — nanoda never saw the export and returned no verdict. Recorded
as a tool gap, not as evidence. (nanoda's acceptance is already established in §3a, on the container.)

**Three things phase C does not do.** It is the same Conductor lineage on the same laptop as phase B, so
it is a stronger *trust* claim, not an independent one — `K1`'s `VERIFIED` still rests on `K2` slot 5.
It moves the end of the trust path from mathlib's oleans to **the Lean compiler binary**, which was
installed by `elan` and not itself built from source. And it says nothing whatever about Theorem 1.1.

**One correction, recorded rather than smoothed over.** Two numbers in this unit are not fully
reconciled, both banked as such in `phaseC.json`: lake reports **11259** jobs where phase B reported
11251 and the prereg expected 11251 (the named target differences do not sum to the +8, and lake counts
jobs it prints no line for); and the prereg's ~20 GB disk requirement was an **underestimate** — the real
tree is 28.5 GB, and ~10.7 GB was freed elsewhere on the volume mid-run by something never identified.
Neither bears on the reading, which rests on the axioms and on rc 0 with 0 errors. `CORRECTIONS.md` §81.

## 4. `K2` (leg 438) — five blind workers, and the label that moved

One file per owner, own branch, cherry-picked unedited into `writeup/data/arc7/k2/r2/`. Support rebuild
banked at `k2/tree_rebuild/` (`runner_rc` 0, 11251 jobs, 2486 oleans, `total_s` 4287).

1. **The five `PARTIAL` statements.** Theorem 3.1 `WEAKER` (item (iv)'s rate `τ^{−A}(e0 + O(τ^{2h}))` and
   the path `r = √(2X_in τ)` absent); Definition 3.3 `NOT-A-THEOREM-IN-LEAN`; Lemma 4.4 `MISSING-CLAUSE`
   (ii); Corollary 7.3 `PRESENT-IN-DIFFERENT-FORM`; Lemma 9.7 `MISSING-CLAUSE`. **Does any missing clause
   weaken the exported statements via the import path: `NO`, for all five** — unanimous across both runs.
2. **The four `sorry`.** Exactly four in code across 2486 project `.lean` files, at
   `ComparatorChallenges/NavierStokes.lean:277,284` and `ComparatorChallenges/Euler.lean:88,184`. Each is
   a Comparator challenge placeholder; **none is in either solution module's import closure** (580 / 1829
   modules). `CONSISTENT` with `K1`'s three banked `#print axioms` runs.
3. **The Comparator's four `NOT-ESTABLISHED` checks, run for real** under a **real `landrun`** built from
   source — the earlier `fake-landrun.sh` deviation is closed, zero `NOT REAL LANDRUN` warnings.
   Check 8 `PASS` (against the network for the first time), check 9 `PASS` (all four exported theorems
   exactly the standard three axioms, no `sorryAx`, **RED not triggered**); checks 0 and 1 stay
   `NOT-ESTABLISHED` — check 1 is *structurally* inapplicable, the JSON carrying neither hashes nor
   statement text.
4. **DeepMind byte-identity, re-verified at upstream source.** `YES`, modulo an enumerated wrapper
   (21 hunks, `MATHEMATICALLY-DIFFERENT` = 0), at both cited pins and at upstream `main` — all three the
   same sha256 `f446284f…d25d`.
5. **Adversarial verifier, blind:** `k1_verdict` = **`VERIFIED-SUPPORTED`**, re-derived from the
   `*_build.log` / `*_axioms.log` primary records rather than the JSON summaries.

**`K1` moved `GREEN, UNVERIFIED` → `GREEN, VERIFIED`** on prereg §4(5)'s condition and nothing else. The
verifier narrowed it itself, and the narrowing is kept: its PART B ran on the same laptop as
`phaseB_local`, so **the second agent added no new machine**, and `#print axioms` reads a compiled
environment, so **this is not a fourth build**.

## 5. `K3` (leg 439) — the construction wave, and the rule that bit back

`K3` re-ran arc 6's wave 4 under one rule: *evidence is a two-route agreement on a quantity the adversary
cannot choose.* Five workers, one blind adversary. Merged: `writeup/data/arc7/k3/merged.json`.

| gate | worker | adversary | integrated status |
|---|---|---|---|
| `Q1` realised stress | `YES` (sup-err 1.71e-14 / 1.54e-14 at `M=256`) | `FAKEABLE` | **NOT EVIDENCE** |
| `Q2` viscous hierarchy `2h` | `UNDER-RESOURCED` | `FAKEABLE` | **NOT ESTABLISHED** (not a `NO`) |
| `Q3` per-stage gain `h/10` | `NOT-INSTANTIATED` | `FAKEABLE` | **DROPPED by the rule** |
| `Q4` leading-order force | 4 cells `NO`, 3 `YES` of 8 | `FAKEABLE` | 4 cells `NO`; the `YES` cells **NOT EVIDENCE** |
| `Q5` `ℬ`'s exact zero | `YES` (`abs_error` exactly 0.0) | `FAKEABLE` | **NOT EVIDENCE** |
| `Q6` flat weight coefficient | — | not attempted | **DROPPED before any run** (§75) |

`counts`: `live_gates` 5, **`EVIDENCE` 0**, `gates_the_blind_adversary_faked` **5**.

**Read this correctly.** A `FAKEABLE` verdict says the gate **as pre-registered** admits a run known to be
wrong — so a `YES` from it is not on its own evidence. It does **not** say the gate's claim is false.
`K3` is a finding about **the gates**, and the three defects behind it are the Conductor's own:

- **`Q5` had no second route.** `experiments/arc6_residual_v1.py:101-103` computes
  `calB_beyond = (2 + 2*h) * (sh - 1.0)` with `sh = 1.0 if heat else 0.0` — algebra in `h` and a boolean,
  reading no field — and route A is the same algebra. Hence `abs_error` exactly `0.0` in all four cells.
  **An error of exactly `0.0` rather than `~1e-16` is the fingerprint of one closed form evaluated
  twice**, now a standing diagnostic. The blind adversary found it independently (its `F5`).
- **The second scale `h = 10⁻³` violates the construction's own validity.** At `λ = 0.1`, Lemma 4.8/(A.6)
  requires `h < min{1/100, λ, e^{−T_d}}` with `e^{−T_d} = 3.0·10⁻⁶`; the builder asserts. The scale check
  asked whether the scale was *resolvable*, never whether it was *admissible*.
- **`Q2` cited Proposition 9.1**, whose own (9.2) table contains **no `q^{2h}` term** — every entry `≤ 1`.

Four disagreements are recorded and **not adjudicated**, including one planted control that did not fire
as planted (slot 3), which that worker reported itself, with a diagnosis. Full record: `CORRECTIONS.md`
§79 and `experiments/journal/leg_439.md`. Standalone note, written for readers outside this
project: [`writeup/notes/PREREGISTERED_GATES_FAKED.md`](../notes/PREREGISTERED_GATES_FAKED.md).

## 6. What arc 7 does NOT establish, said once, plainly

- **Not** that the Navier–Stokes problem is solved, by anyone. The Clay prize has four conditions; none
  is met.
- **Not** that the manuscript is correct. Nothing measured here contradicts it; nothing measured here
  proves it.
- **Not** that the kernel check settles Theorem 1.1. The Lean statement is Fefferman (C)/(D), strictly
  weaker, with five existence clauses absent.
- **Not** that the Lean proof follows the paper's argument.
- **Not** that mathlib itself is correct. As of 2026-09-11 mathlib *is* compiled from source here, so
  the earlier caveat "not that the cached oleans mean what their sources say" is **closed** (§3b) — but
  the trust path now ends at the Lean compiler binary, which was installed, not built from source.
- **Not** that `K3`'s zero says anything against the manuscript. It says the gates were fakeable.
- **No position whatsoever on the priority dispute.**

**No wall moved. No `L1→L4` link moved — still, after 440 legs. Tier 2 is never a proof. Clay ~0.05%.**

## 7. Verification status, per unit — not averaged

| unit | status |
|---|---|
| `K1` kernel check | **GREEN, `VERIFIED`** — by `K2` slot 5, blind, on prereg §4(5)'s condition and nothing else |
| `K1` olean integrity | **ESTABLISHED**, two independent kernels; same lineage, so `UNVERIFIED` by a second agent |
| `K1` olean semantic match | **ESTABLISHED** 2026-09-11 (§3b) — mathlib rebuilt from source, cache never consulted, axioms byte-identical; same lineage, so `UNVERIFIED` by a second agent |
| ~~`K1` semantic match~~ | **STRUCK 2026-09-11 — duplicate of the row above.** It read *"OPEN, costed, not run"*; that was the same limit, and phase C closed it (§3b). Left struck, not deleted: it was the published status until that day |
| `K2` gate answers | five blind workers agreeing across two runs; the Conductor's integration is `UNVERIFIED` |
| `K3` gate answers | **`EVIDENCE` 0**; every gate `UNVERIFIED` |
| `K4` this document | `UNVERIFIED` — Conductor-written |

## 8. Defects of this arc, recorded

`CORRECTIONS.md` §72 (charter vs board), §75 (`Q6` mis-scaled, dropped before any run), §76 (the olean
claim split three ways), §77 (two banked job counts off by one), §78 (three `K2` prereg wording defects),
§79 (three `K3` prereg defects, all the Conductor's). The §3g step-1 ordering — pre-registration and wave
row pushed **before** dispatch — held for `K2`, `K3` and `K4`.
