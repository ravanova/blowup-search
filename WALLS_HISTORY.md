# WALLS_HISTORY — retracted and superseded text from `WALLS.md`, kept struck rather than deleted

Split out of `WALLS.md` on 2026-08-18 under §3j (headroom), struck text intact. Referenced from
`WALLS.md` as `## History`. **Nothing here is live.** A claim in this file has been retracted or
superseded by a measurement; the measurement that did it is named in place.


**§3j's remedy for this file's cap.** Nothing below is live; it is retained because a wall's history
is the point: a reader who finds only the corrected claim cannot tell whether it was ever wrong.
Full elaboration is in the journals and in git.

## W2's crack and Lane T's item 3 — the same claim, struck

> ~~Leg 348 located `arXiv:1902.00384` — **a certified periodic orbit of 3D Navier–Stokes with the
> viscous term inside the certified equation, on the three-torus.** Natively 3D, natively
> time-dependent, genuinely viscous, genuinely fluid. Not a blow-up, so it does not fill leg 174's
> Grade-A/fluid **blow-up** cell — but the *technology* clears W2's bar already, and only the
> *target* is missing.~~

**RETRACTED by `T4` / leg 393 (`2c87244`)**, from the authors' own data package, not from prose:
`N_x3 = 0`, arrays of extent 1 in `x₃`, `max|u⁽³⁾| = max|ω⁽¹⁾| = max|ω⁽²⁾| = 0.0` exactly against
`max|ω⁽³⁾| = 1.6351 / 1.5274` (so the zeros are structure, not an empty array), `setup = '2D'`; the
authors give the reason — a 3D solve's memory cost is *"for now, prohibitive."* **Certified by
exactly the banned apparatus besides**, and **VERIFIED by `V-W2`** from a re-fetched artefact whose
SHA-256 matched the banked digest. Leg 348 read it at abstract level and flagged that limit itself.
Detail: `experiments/journal/leg_393.md`.

## The `2409.09234` census correction, and the Conductor-wording defect inside it

**The ground is the FIRST clause, not the second** — this file and the dispatch quoting it had them
the wrong way round. **(i) PRIMARY**, `T6` verbatim: *"THIS PAPER CLOSES NO TAIL-DOMINATION ESTIMATE
AND IS NOT AN INSTANCE OF THAT TECHNOLOGY AT ALL"* — a theorem about a **1-D map fitted to DNS
data**; `V-W2` re-measured all five term counts at **0**. **(ii) SECONDARY**, *struck:* ~~"no-slip
walls, not periodicity"~~ — the paper never says *"no-slip"* and states moving-wall Dirichlet with
*"periodicity … enforced to the rest of boundaries"* (§2 p.4). **Count unchanged: 6 − 1 = 5.**
**Second Conductor-wording defect a verifier caught** (`V1` caught the first, on `R0`'s comparand);
**neither found by the Conductor.** Detail: `experiments/journal/verify_wave2.md`.
