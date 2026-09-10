# Arc 6 Lean build logs — banked VERBATIM 2026-09-10 (leg 437, arc 7 K1), copied from the session scratchpad that produced them

These are the raw logs behind `kernel_check_conductor.json` (leg 435) and the leg 418/431 build gates. Nothing edited; mtimes in the table are the scratchpad's. Clone HEAD `8937a8f4`, toolchain `leanprover/lean4:v4.34.0-rc2`, mathlib `85e3a25e`.

| file | leg | what it is |
|---|---|---|
| `lean_build_attempt1.log` | 418 | first `lake build` attempt (2026-09-09 16:34), mathlib from source, cache host denied |
| `lean_cache.log`, `run_build.sh` | 418 | the `lake exe cache get` attempt and the runner that chained it |
| `lean_build.log` | 418 | the long from-source mathlib build (2026-09-09 17:18), killed at the leg's cap |
| `chain_build.sh` | 418/431 | the chaining script: wait for cache get, then `lake build` |
| `cache_get_leg431.log`, `lean_build_leg431.log` | 431 | agent 1's cache get (host reachable) and its 13.6-min build (stopped by the Conductor's mis-stated cap, leg 431 §3.1) |
| `kernel_check_leg431.lean`, `ps_check_leg431.lean` | 431 | the `#print axioms` files that failed with "object file … does not exist" |
| `lean_chain_leg431.log` | 431→435 | the Conductor's continued build: cache get to completion (`06:24Z`), then `lake build`; last line `[10526/11251]` when the session ended — Euler unfinished |
| `kernel_check_leg432.lean`, `kernel_check_leg432.log` | 435 | the file and the verbatim output of the kernel check at `08:05Z`: both exported theorems on `[propext, Classical.choice, Quot.sound]` |
