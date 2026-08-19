# WAVE 8 — LANDINGS AND THE §3i DIRECTION CHECK, ONE BLOCK PER UNIT AS IT RETURNS

§3i is run **every time a unit returns**, not once per wave. The wave is NOT closed while this
sentence is here: `L-JVER` (409), `PB1` (411) and `V-W7` (412) are in flight, and `E-FE` (408) is
a LATE RETURN whose verdict **may not influence this wave's ranking** (ruling `99421dd`).

---

## LANDING: `PB2` (leg 410, `a7ffa1e`) — **GATE `YES`**, and the jaw closes on a DIFFERENT THEOREM from the one the wall cites

### The gate, in its pre-committed wording (`WAVE8_PLAN.md` AMENDMENT 4)

> For the route-4 object as `L5` actually constructs it: **which named theorem excludes it at
> `ṁ ≡ 0`, and does that object satisfy that theorem's stated hypotheses?**

**Answer: `YES`. Tsai 1998 Theorem 2 carries it, and the object satisfies its hypotheses.** This is
AMENDMENT 4's **first** pre-committed reading, which was written down as *"a good outcome and the
likeliest"*: clause (b) STANDS and the `WALLS.md` citation was under-specified.

### What I verified myself, at primary, rather than taking from the unit

| claim | how I checked it | result |
|---|---|---|
| Tsai's hypothesis sentence | `pdftotext -layout Papers/TSAI1998.pdf`, line 236 | **exact**: *"we do not require the weak solution `u` to be a Leray-Hopf weak solution. Our only requirements (apart from self-similarity) are (i) and (ii): the Navier-Stokes equations and the local energy estimates."* |
| Theorem 2's statement | same extraction, lines 131–133 | **exact**: local energy estimates `(1.4)` in `Q₁(0,T)` + form `(1.2)₁` ⟹ `u ≡ 0`. **No `L^q`, no Leray–Hopf, no boundary condition.** |
| Theorem 1's statement | lines 128–129 | `U ∈ L^q(ℝ³)`, **`q ∈ (3,∞]`** ⟹ constant, zero if `q < ∞`. The range is **open at 3**, as leg 364 said. |
| NRŠ's actual reference | Tsai's own bibliography, `[NRS]` | **`Acta Math.` 176 (1996), 283–294** — verbatim. The repository's *`ARMA` 136 (1996) 55–98* is wrong in journal, volume and pages. |
| NRŠ's hypothesis | Tsai's introduction | *"the main result of `[NRS]`"* is for a weak solution **belonging to `L³(ℝ³)`** — exactly `q = 3`, the case Thm 1's range excludes. |
| the log-divergence arithmetic | recomputed: `60.4916579840 × ln 10` | **`139.28719`** against the banked `139.287`, rel. `1.4e-06`. The coefficient and the per-decade increment are consistent. |
| the `1021`-line residual | `wc -l` = **1002**, `grep -c $'\f'` = **19**, `pdfinfo` = **Pages: 19** | `1002 + 19 = 1021` **exactly**. Resolved, not `UNVERIFIED`. |
| hashes | `sha256sum Papers/TSAI1998.pdf` | `6d3182d5…` **matches** the leg-359 pin |
| territory | `git show --stat a7ffa1e` + `git log --all -- <artefacts>` | 6 files at landing, artefact and runner tracked at the earlier checkpoint `c98af80`. **Zero deletions in `WALLS.md`** — the `V-W5`-verified sentence is untouched, as the unit claimed. |
| the evidence suite | re-ran `p2_route_pb2_v1_evidence.py` | **31/31, exit 0** |

**So the substance holds and I am not qualifying it.** `W4` clause (b) is on a **stronger** footing
than its own citation implied: the theorem that carries it is one this repository holds at `FULL
TEXT`, and the source it has failed to obtain four times — NRŠ — **is not load-bearing for this
clause at all**, because the object is not in `L³`.

### Three things the unit did not check, and the first two are mine

**1. `WALLS.md` landed 2,151 BYTES OVER its §3j cap, through a `MERGE GATE: PASS`.** The unit added
25 lines; the file went 32,526 → 34,919 against a cap of 32,768. My `WAVE8_PLAN.md` §6 STANDING
CLAUSES — the block whose stated purpose is *"IN EVERY BRIEF"* — **does not mention §3j**, and the
merge gate has never checked it. **I had measured that cap by hand ninety minutes earlier and then
treated the number as a standing property.** `CORRECTIONS.md` §48. **Remedied by construction**:
`test_headroom.py`, wired into `scripts/merge_gate.sh` as an always-on check, mutation-tested on
four breaks — file over cap, row over 600 chars, LIVE block over cap, LIVE heading missing (which
it fails rather than skipping, because an unchecked cap is not a passed cap). Caps restored by
**verbatim retirement**, five blocks, nothing compacted and nothing deleted.

**2. The evidence script is 0 of 31 `recompute-from-primary`.** It imports `json`, `sys`, `pathlib`
and nothing else; all 31 checks re-read the artefact the unit itself wrote. The brief required
every check to carry its class; **the script carries zero labels and nothing checked that it did.**
But the deeper finding is not the unit's fault: `ORCHESTRATION.md` §6 clause 3 **requires** evidence
scripts to rebuild from the JSON *"without re-running anything"*. §45 called this drift across 32 of
49 scripts. **It is not drift, it is compliance** — the contract specifies a check that cannot fail
on the error class it exists to catch. `CORRECTIONS.md` §49. **The clause is not withdrawn**; it
has a real purpose, and amending an orchestration contract is a user decision, not mine.

**3. The citation defect is in FIVE places, not four.** The fifth is
`experiments/p2_route_l5_v1_driver.py:640` — **the generator of the fourth**. `PB2` searched the
prose and the banked JSON and found every occurrence there, but not the code that writes the JSON.
Driver corrected; the banked JSON left alone under the W3 Q3 ruling, with the divergence declared
in the driver itself. **And `WAVE8_PLAN.md` AMENDMENT 4, which I wrote to scope this very unit,
asserts the wrong citation in its own jaw table.** `CORRECTIONS.md` §47b.

### The quartet, priced not silently dropped

No `BLOG_*`/`TECHNICAL_*` pair (~1 h) and no registered figure (~15 min), following leg 364's
literature-unit precedent. §6's merge-gate rule is not tripped because neither was shipped. **This
is a recorded debt, not a discharge.**

### §3i — THE SEVEN, answered against the RECORD

**1. Did this unit move an `L1→L4` link?** **NO.** It verifies that a hypothesis of a published
theorem is met by a synthetic float64 profile. It proves no theorem. Tier 2. Clay stays ~0.05%.

**2. What did it make FALSE?** (i) That NRŠ is load-bearing for `W4` clause (b) — **it is not; its
`L³` hypothesis is not satisfied by this object.** (ii) That the two theorems in `WALLS.md`'s
clause-(b) sentence are interchangeable — **only Tsai Thm 2 applies as stated.** (iii) That NRŠ is
*ARMA* 136 (1996) 55–98 — **it is `Acta Math.` 176 (1996) 283–294.** (iv) `SOURCES.md` row 1's
`1021`-line residual as an open discrepancy — **resolved arithmetically.** (v) That the §3j caps
were being enforced — **they were not, and now they are.**

**3. Does Lane L still deserve its rank ON WHAT IS MEASURED NOW?** **Yes, and slightly more so.**
The clause the pivot was worried about is not merely still shut; it is shut on a source held at
`FULL TEXT` rather than on one at `SECOND HAND`. **W4's only unbroken clause remains (c)**, which
is Lane T's and deferred. Nothing here promotes another lane.

**4. Is any live claim resting on a source whose own recorded ceiling is undischarged?** **Yes,
and `PB2` narrowed it rather than closing it.** NRŠ 1996 is `UNREACHABLE` at primary for the fourth
independent time — **now with the positive network control leg 364 lacked** (arXiv HTTP 200;
Springer login wall; Euclid stub), so the refusal is the publisher's, not the container's. **Its
price against clause (b) is now ZERO.** It is *not* zero for `solver/dssp_screen.py`, whose `q = 3`
screen still cites Tsai Thm 1 — a range that excludes `q = 3` — and still rests on `SECOND HAND`.
**That is leg 364's finding, unchanged, and it does not touch this clause.** ESŠ remains
`UNREACHABLE` and carries the `α ≤ 1` half of the pin through Seregin.

**5. What is the CHEAPEST unit that could KILL the priority lane, and why is it not next?** Still
`L-JVER`, and it **is** running: if `J(c)` as coded is not the norm it is claimed to be, every
route-4 residual number in the lane is void, including this one's context. `PB2` does not change
that ranking; it is a literature unit and Lane R/paper units never set direction.

**6. If Lane L were dead tomorrow, what would we do instead — and is it cheaper?** Unchanged from
`L6-b`'s answer: Lane T's clause (c), which is deferred by user ruling and is not mine to un-defer.
`PB2` makes the alternative slightly *less* attractive, because it strengthens the case that (a)
and (b) are genuinely shut rather than shut on a citation.

**7. Are we in an audit/instrument loop? Count the last three units by kind.** `L6-b`
(**construction**), `R-prof` (**instrument**), `PB2` (**literature/audit**). One construction in
three, and the wave in flight opens with `L-JVER`, a construction. **Not a loop, but the margin is
thin, and note that this integration itself produced one construction (`test_headroom.py`) and
three corrections — the ratio the §3i q7 clause exists to watch.**

### RE-RANK: **NONE.**

Nothing in `PB2` changes the ordering. `L-JVER` → `L6-e` → `L8` stands. The one thing that would
have forced a re-rank — the second or third pre-committed reading, where clause (b) turned out to
depend on an unmeasured `L^q` membership or could not be determined — **did not fire**, and the
reading that did fire is the one AMENDMENT 4 called the likeliest before the unit ran.

**Ceiling on all of the above: Tier 2, float64, a measurement on `L5`'s synthetic `α = 1` profile.
Route 4 has no banked profile of its own here. No `L1→L4` link moved.**
