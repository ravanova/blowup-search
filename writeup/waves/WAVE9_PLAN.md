# WAVE 9 — PLAN. Committed BEFORE dispatch (`ORCHESTRATION.md` §3g).

**Opened 2026-08-19 by the Conductor. Wave 8 closed at `024a9b2`/`c63769b`.**
Legs 413–416. `E-FE` (leg 408) remains in flight as a late return and **may not influence any
ranking in this plan** (ruling `99421dd`).

## THE COMPUTE FACT THAT SHAPES THIS WAVE, STATED NOT HIDDEN

Measured at planning time: **load average 26.5 on 12 cores.** `E-FE` has **9 shards alive and is at
47/160** as of 08:57Z, which re-prices it at **~20 h remaining, not the ~15.2 h banked at dispatch**.

**Consequence, and it is a scheduling decision, not a scoping decision:** `L6-e` v2 — the highest
unit in Lane L and the one whose gate is already pre-committed at `CORRECTIONS.md` §53 — is
**PLANNED, PRICED AND HELD FOR CORES**, to be dispatched the moment `E-FE` returns. Running a
20–35 core-h optimisation against a box at 2.2× oversubscription would take 3–4× its price *and*
delay `E-FE`, and `R-prof`'s `MACHINE_WAS_NOT_QUIET` would contaminate any timing in it.
**It is not descoped, not deferred indefinitely, and not replaced by something smaller.**
`§3g`'s composition floor is met by `L5-cmod`, which is a Lane L unit on the Clay chain.

---

## UNIT 1 — `L5-cmod` (leg 413). LANE L. CONSTRUCTION. **The wave opens with it (`§3f` rule 3).**

**Why now.** It is the single unadjudicated flag left by §53, it is cheap, and it bears on a number
(`c_mod = 869.288`) that `L5`'s W4-clause-(b) work and `P2`'s draft both quote.

**THE GATE, pre-committed.** Extend `L5`'s cutoff-radius sweep on the load-bearing row
(`α = 1 | κ = a_physical_frozen | DSS`) from `ρ ≈ 1.26e3` out to **`ρ = 1e8`**, same apparatus, same
norm `‖curl F‖_{L¹_t L^{3/2}_x}`, `L5`'s code READ NEVER MODIFIED. Report the increment in `c_mod`
**per decade of `ρ`** for every band.

> **Is the per-decade increment approaching a NONZERO CONSTANT — YES or NO?**

**THE PRE-COMMITTED READINGS.**
- **YES** ⟹ `c_mod` is **logarithmically divergent**, `869.288` is a value of `L5`'s cutoff and not
  of the functional, and §53's flag is DISCHARGED AS DIVERGENT. `L5`'s gate answer `NO` is
  **strengthened** (a growing error is further above threshold), and this must be written that way
  and **not** as a retraction. `P2` may not quote `869.288` without the disclosure.
- **NO**, increments continue to decay toward zero ⟹ `c_mod` genuinely saturates, `L5`'s original
  reading was right, and §53's flag is DISCHARGED AS SATURATING. **This is a good result and it must
  not be written as a null.**
- **Increments neither settle nor decay within reach** ⟹ `UNDER-RESOURCED` with a price. **NEVER a
  `NO`.**

**Ceiling to write BEFORE the answer:** whichever way it falls, no `L1→L4` link moves, Tier 2,
float64, and it says nothing about whether a blow-up profile exists.

---

## UNIT 2 — `P4-DRAFT` (leg 414). PAPER. ADDITIONAL, not a substitute.

Draft `P4` (methodology). **`writeup/papers/P4_METHODOLOGY/STATUS.md` now carries twelve entries and
an honest tally of 2 prospective against 9 retrospective — that tally goes in the paper.**

**BINDING, from the user directive.** A paper is a **VIEW OF THE RECORD, NEVER A SOURCE**. Every
number cites its banked JSON field. UNVERIFIED stays UNVERIFIED. UNDER-RESOURCED is not written as a
null result. A control that did not fire as planted is disclosed. **No unit may cite a draft.**
**PROHIBITED:** writing `P4` as a tour of the repository; reporting only the catches. **It needs an
honest account of what the discipline FAILED to catch and for how long — and entry 11 (§51, missed
for eleven legs by unit, Conductor and verifier alike) is the centre of gravity, not an appendix.**
§3k rule 3 applies hardest here: **name the existing practice** (pre-registration, adversarial
collaboration, computer-assisted-proof reproducibility norms) or the paper reinvents it.

**Second output, which is not the paper:** `FINDINGS.md`. Expect it to be worth more than the draft.
**Say so if it is.**

---

## UNIT 3 — `P2-DRAFT` (leg 415). PAPER. **Unblocked because `PB2` cleared, gate `YES`.**

`PB2` discharged §3k rule 2 by reading both jaws at primary. `P2` may now be drafted past its claim
statement.

**HARD CEILING, verbatim from the user directive — `P2`'s contribution may not be written as larger
than:** *"the identification of `T₃` as the sole survivor and its `ṁ`-proportionality, in float64, on
a synthetic profile."*

**And it must disclose, not smooth:** that `W4` clause (b) rests on **Tsai 1998 Theorem 2**, not on
the citation the repository carried for months (`CORRECTIONS.md` §47/§47b — the wrong reference
survived in FIVE places including the generator); that **NRŠ does not apply** because `∫|U|³` is
log-divergent at `α = 1`; and that **`c_mod = 869.288` is under an open §53 flag** whose resolution
is `L5-cmod`, running in this same wave. **If `L5-cmod` returns YES, that goes in the draft.**

---

## UNIT 4 — `V-W8` (leg 416). VERIFIER. **Dispatched LAST (`§3f` rule 3).**

**I PLANNED WAVE 8. I MAY NOT VERIFY IT.** `V-W8` verifies `PB2`, `PB1`, `V-W7` and `L-JVER` against
their pre-committed gates, **and it verifies the Conductor's integration commits** `54b755b`,
`233a2c3`, `024a9b2`, `c63769b`.

**Specifically instructed to attack, because these are mine and they are load-bearing:**
1. **§53's central arithmetic.** Re-derive the per-decade increments from
   `p2_route_ljver_v1.json` `cutoff_sensitivity`. Is the "three bands inside 1%" claim true?
2. **§53's SIGN claim**, on which every surviving `NO` now rests. Is *every* increment positive?
   **If a single negative increment exists at any reach, say so — it would reopen `L6`, `L6-b` and
   `L5` simultaneously and that is the most consequential thing you could find.**
3. **§53's ×130 separation** of §52 from §51. Is `6.22e-5` against `8.06e-3` the right comparison,
   or have I compared quantities that are not commensurable?
4. **§50 item 6.** I ruled `V-W7` "UPHELD IN PART" and kept a sentence it called false. Was that a
   correct ruling or a Conductor protecting his own wording?
5. **The §51/§52 block placement.** I landed them under W7, moved them to W4, and said W7 was
   intact. **Verify W7 is byte-identical to before my edits.**
6. **Every verbatim retirement this wave** — `§W-LANEL-FIRSTTWO`, `§OPTIONS-L7`, `§OPTIONS-L4`,
   `§STATE-W67-L6`, `§STATE-PIVOT-FLOOR`, `§OPTIONS-R6R7`, `§W4-A-PROV`, `§STATE-W7-RBANK-RPROF`,
   `§STATE-W6-V5` — line-count and byte-identity against what was removed.
7. **`test_headroom.py` itself.** It is prospective and I wrote it. Mutate it and show it fails.

**A defect found in my work is the expected output of this unit, not an accident of it.**

---

## STANDING, ON EVERY BRIEF

**COMMIT DURING THE RUN, NOT ONLY AT THE GATE.** Checkpoint above ~1 h. Explicit paths only; no
`git add -A`/`add .`/`commit -a`, no `checkout`/`stash`/`reset`/`rebase`, no push. Siblings share the
working tree — **`CORRECTIONS.md` §50 item 4: a commit subject that does not name the files it
carries silently reassigns their provenance.** **NEVER read `DIRECTION.md`.**
**Tier 2 is never a proof. Scale is not evidence. No output is movement toward Clay unless a link
actually moved — Clay is ~0.05%.** Reading published material is authorised; **contacting any
author, group, maintainer or list REMAINS HELD.**

## HELD FOR CORES, DISPATCH ON `E-FE`'s RETURN

**`L6-e` v2 (Lane L, ~20–35 core-h).** Gate pre-committed at `CORRECTIONS.md` §53, unchanged by this
plan: re-run rung `J3` (`Lmax 3, Nr 16, Ks 2`, 2400 dof) to 20,000 iterations; report `ρ(J3@20k)` at
`J3`'s native `nq_r = 60` **and** at `J4`'s reach `nq_r = 72`; the ladder inverts iff the **matched**
value falls below `1.504851895102804`; if the two straddle it, the ladder is undecidable at this
reach **and that is the result**; also report the far-field increment per decade at the new iterate.
