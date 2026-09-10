# ESCALATION — leg 251's named Phase-1 target: does construction get the go?

**Raised** 2026-08-06 by leg 251 (Route-P0T), which escalated rather than landed.
**Carrier until 2026-09-10:** GitHub PR **#20**, now CLOSED UNMERGED. The work is preserved on the
pushed branch — see §5. Closing the PR retired the *carrier*, not the question.
**Status: OPEN. RECORDED, NOT RULED.** Promoting an exploration route into the committed sequence is
`ORCHESTRATION.md` §8 escalation 1, which is the user's signature and never the Conductor's.

---

## 1. The gate, in its own pre-committed wording

`DIRECTION.md` leg 251 / `CONTINUATION_PROMPT.md` Directive 1 asked:

> *Does at least one target object + ansatz combination survive BOTH the NRS/Tsai screen (not
> excluded) AND a check against every already-banked dead end in this repository's own record (not a
> re-proposal of something already measured dead)?*

**The leg answered YES** — six of fourteen survive, four unconditionally. Its own journal states the
consequence plainly: *"the yes-branch of this leg's own gate is an escalation by construction."*
Fourteen pairs screened; five killed at the NRS/Tsai stage, five at the banked-dead stage, three by
each screen alone.

## 2. The named candidate

**Object.** 3D isentropic **compressible** Navier–Stokes, density-independent viscosity, `γ = 7/5`.
**Ansatz.** The smooth radially symmetric self-similar imploding profile `(U^E, S^E)` — BCG
`arXiv:2208.09445` Thm 1.2, blow-up conclusion at Thm 1.3; non-radial companion CGSS
`arXiv:2310.05325`. **As corrected by legs 265 and 275 the ansatz names `n = 3`, not "n odd and
large"** — see `ESCALATION_PHASE1_COSTING_2026-08-07.md` §2, and §4 below.

Five obligations a certificate must discharge are stated in the journal and were left byte-identical
by both correction legs.

## 3. The question, stated so it can be answered Y or N

**Q. Does the leg-251 candidate get the go as the Phase-1 construction target — Y or N?**

- **Y** promotes an exploration route into the committed sequence. That is escalation 1 in §8 and
  requires the user's signature; it is not implied by the gate's YES.
- **N** leaves the cell that leg 174 opened — **Grade-A × fluid-adjacent** — still empty, as leg 242
  recorded it: *"— STILL EMPTY —"*.

## 4. What this does NOT establish, kept from the leg's own ceiling

- **No link of the L1→L4 chain moved. Clay odds stay ~0.05%.**
- The candidate is **compressible** Navier–Stokes — **not the system Clay asks about**.
- The leg establishes the target is *unclaimed* and *un-excluded*, **not** that it is feasible.
  Feasibility is Phase 1's job and this leg attempted no certification.
- **Wall 2 is not crossed.** The 3D-ness comes from a spherically-symmetric ODE profile.
- NRS 1996 remains **unread at source** (5 failed routes), tagged `restated_by` throughout.
- Two corrections the leg made to the repository's own screen are carried with it: that
  "unstable-self-similar with a finite unstable spectrum" is **excluded, not a survivor** (Tsai 1998
  Thm 1 is stability-blind), and that **Tsai's hypothesis is a GROWTH condition, not a decay
  condition** — against which 19 in-repo sites say decay.

## 5. Where the work is

Branch **`leg/251-p0t-v1`**, head **`2aac47aafc6d67fa4f3011321ee2a7794ff6a672`**, 5 commits, never
merged to `main`. Eight files, 2,917 insertions:

| file | |
|---|---|
| `experiments/journal/leg_251.md` | the leg |
| `experiments/journal/leg_266.md` | Route-P0TC — re-poses obligation 1 (§4 below) |
| `experiments/journal/leg_275.md` | Route-P0TC2 — applies leg 265's ansatz correction |
| `experiments/p2_route_p0t_v1_targetselection.py` | the runner (a ledger; no compute) |
| `writeup/data/p2_route_p0t_v1_targetselection.json` | the ledger |
| `writeup/novelty/leg_{251,266,275}.md` | novelty passes, each committed before its runner |

**Legs 266 and 275 exist ONLY on this branch and are on no other record.** Leg 266 re-poses
obligation 1: at BCG's scaling the *"solution of the self-similar profile system of the dissipative
equation"* **does not exist**, because the stationary system BCG solve is the **Euler** system.
Leg 275 applies leg 265's `n = 3` correction to the report. Neither changes leg 251's gate answer.

## 6. Why nothing was stopped while this is open

Work did not stop and has not stopped: arcs 5, 6 and 7 ran to completion after this was parked, and
arc 7 closed on 2026-09-10. Under §8 the Conductor parks the item, refills the slot, and keeps every
other leg moving. Nothing downstream of this escalation was built, so **N costs nothing already
spent**.
