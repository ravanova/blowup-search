# Leg 57 — Route-XS v1: the shape dichotomy against published certificates

**Branch** `leg/xs-v1`. **Exploration leg** (not critical path). **Sharding experiment:
the LEG-D control arm** (`ORCHESTRATION.md` §10). **Gate: NO.**

---

## Order of work (the discipline, as executed)

1. `plan_of_record.py` — read. `MM` is NEXT; every live ban noted, in particular the two
   that bind this leg: *no further `ℓ¹`-Fourier machinery for this operator before MM's
   gate answers* (this leg builds none — it measures an operator that already exists), and
   *grep `capabilities.py` before building anything* (done; see 3 below).
2. `CONTINUATION_PROMPT.md` — read in full, lessons 84–90.
3. `DIRECTION.md` — **has no leg 57 entry.** The file is still the SEED (status line: *"no
   queue yet"*, last leg number 53). The thesis and the verbatim gate came from the
   dispatch prompt instead. **Flagged for the orchestrator: the DM has not yet written the
   queue that ORCHESTRATION §10 requires for the sharding experiment's pre-registered
   difficulty class.** Without that pre-registration the A/B/C-vs-D comparison is
   confounded, which §10 itself says makes it worthless.
4. **Novelty pass FIRST**, committed before any construction
   (`writeup/novelty/leg_57.md`, commit `5814a4f`). Six queries, **links not counts**.
5. Full-text pass, then module, tests, runner, data, figure, writeups.

## What the novelty pass changed about the leg

Verdict **`PROCEED_AS_BOOKKEEPING`**, and it demoted the deliverable before it was built.
Cadiot arXiv:2505.03091 states **both halves** of the dichotomy in print (§2: the operator
"becomes an infinite diagonal matrix"; §3: `D` "is supposed to be diagonally dominant").
So the leg classifies known practice rather than discovering it, and the writeups say so at
the top rather than in a caveat at the bottom. This is the ban from legs 51/53 holding.

**Leg 52's search-index flag is NOT cleared.** Q5 returned arXiv:2604.01868, but Q5 is a
*different* query from leg 52's verbatim one. Leg 53 was withdrawn for exactly this move
and I am not repeating it.

## Papers actually read at full text

`bash Papers/fetch.sh` → `1503.06315`, `2302.12877`, `2410.05480`, `2210.07191`,
`2305.05660` (Chen–Hou Part II, already present), plus `2505.03091` fetched directly.
Egress worked on the first attempt (arxiv.org HTTP 200).

**One wasted fetch, recorded so nobody repeats it:** I guessed `2306.09214` for Chen–Hou
Part II. It is an unrelated medical paper (blood–brain barrier). **Part II is 2305.05660**,
which was already in `Papers/`.

## What was reused rather than rebuilt (the capabilities ban)

`solver/spectral_certificate.py` already had `tail_block`, `tail_inverse_norm`,
`bordered_tail_inverse_norm` and the `mu` dissipative control. **Nothing was rebuilt** —
`solver/certificate_shapes.py` imports them. The one genuinely new idea is that **`mu` is
already a continuous dial from shift to multiplier**, and that BDL's ratio `δ` equals
`1/(2·mu)` on this operator. That reading cost no new code at all.

## Results

* **Gate: NO.** 0 of 4 published rows is a counterexample. The predicate flips to **yes**
  on a fictitious control row (lesson 90), so the "no" is about the literature.
* **11 located full-text statements** across 4 rows; `unlocated_rows()` empty, tested.
* **The measured dial:** `mu = 0` alone fails — `M`-exponent **+1.021** (unbordered inverse
  does not exist), and once bordered the `K`-exponent is **+0.437** (it GROWS). Every
  `mu > 0`: `M`-exponent 0, `K`-exponent **−0.849 … −0.946**.
* **Sharpens legs 52–53:** the bordered tail inverse is **not a constant**. It runs
  **2.191 → 11.528** over `K = 4 … 128` (**5.26×**). The 2.19 those legs quote is the
  smallest rung of a rising ladder, not a bound.
* **BDL is the near-miss that matters for MM:** a published **non-block-diagonal**
  approximate inverse (Prop 2.3 gains the full `s_L`) — but only under assumption (4), a
  diagonal bounded below.
* **Chen–Hou is the confirmation, not the counterexample:** the only published CAP with a
  shift unbounded part, and it forms no tail estimate at all (§2.7, damping from advection).

## The hypothesis that died

BDL's `δ < 1/2` reads `mu > 1` here, so the transition should have been at `mu = 1`.
**REFUTED:** `mu = 0.25` (`δ = 2`, four times outside BDL) is boundedly invertible and
decays at −0.849. `δ < 1/2` is what BDL's LU construction needs, not where the operator
changes character. Kept as test 14.

## Mistakes made in this leg, kept visible

1. **The `mu = 1` hypothesis** above — posed, measured, dead. In the artifact as
   `XS4_dead_hypothesis`, verdict `REFUTED`.
2. **Bordering a `mu > 0` tail** to compare across `mu`. Produces 1.06e+03 … 8.26e+04 and
   means nothing — leg 53 already banked this trap (bordering an already-invertible
   operator with the wrong near-null pair). Caught before it reached the prose; kept as
   `XS5_wrong_operator_control` (lesson 76).
3. **Wrote the test file for pytest first.** The repo has no pytest and
   `requirements.txt` is numpy + matplotlib only; the convention is plain asserts with a
   `__main__` runner. Rewritten to match.

## Environment notes for the next agent

* **`.venv` lives in the main repo, not in the worktree.** `.venv/bin/python` fails from a
  worktree; use `/home/andy/projects/Unsolved/.venv/bin/python`.
* **pytest is not installed anywhere.** Do not write pytest tests.
* Worktree isolation refuses compound shell commands with redirects that it cannot verify
  stay inside the worktree — break them into separate plain commands.

## Artifacts

| what | path |
|---|---|
| module | `solver/certificate_shapes.py` |
| gates (15/15) | `test_certificate_shapes.py` |
| runner (221 s) | `experiments/p2_route_xs_v1_shapes.py` |
| data | `writeup/data/p2_route_xs_v1_shapes.json` |
| figure | `writeup/figures/fig52_route_xs_v1_shapes.png` (registered in `build_figures.py`) |
| evidence script | `experiments/p2_route_xs_v1_shapes_evidence.py` |
| technical | `writeup/4_p2_lottery/TECHNICAL_P2_ROUTEXS_V1.md` |
| blog | `writeup/4_p2_lottery/BLOG_P2_ROUTEXS_V1.md` |
| novelty log | `writeup/novelty/leg_57.md` |

**No link of the L1→L4 chain moved. Clay stays ~0.05% behind Walls 1 and 2.**
