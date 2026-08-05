# Leg 67 VERIFY — independent re-check of the Route-FD novelty pass

**Date:** 2026-08-06. **Branch:** `verify/67-fd-review`. Post-landing review of a claim-bearing,
literature-only leg. **Verdict: PASS with two precision caveats, no rework required.**

The full line-by-line record is in `experiments/journal/leg_67_verify.md`. This file records the
novelty-side conclusion: what was re-fetched from primary source, what was reproduced
independently, and what the negative result does and does not establish.

## What I re-fetched myself

I did not rely on leg 67's `Papers/` extraction. arXiv:2606.03680 was fetched fresh
(abstract page and full-text HTML), as were the abstracts of arXiv:2601.02464, arXiv:2604.01868
and arXiv:1908.09385.

**arXiv:2606.03680 — Stefanov, Wu, Xu, Ye, *Global regularity of the 2D fractional Boussinesq
equations with subcritical dissipation*.** Real paper, exact title and author list as cited,
dissipation `(-Δ)^{α/2}u` and `(-Δ)^{β/2}θ` as cited. Every §1 sentence leg 67 quotes verbatim is
verbatim:

- the Jiu–Miao–Wu–Zhang classification into subcritical `α+β>1` / critical `α+β=1` /
  supercritical `α+β<1`;
- "In the special case α+β=1, the Boussinesq regularity problem boils down to the corresponding
  problem on the generalized surface quasi-geostrophic equation with critical dissipation" — this
  is the vorticity-stream-equivalent half of the gate and it is quoted correctly;
- "the global regularity problem for the supercritical regime remains largely out of reach";
- "how much dissipation is required to ensure global regularity?";
- the full ladder on the critical line — `0.9132`, `0.7981`, `0.7692`, `2/3` — plus
  Constantin–Vicol, Chae/Hou–Li, and Hmidi–Keraani–Rousset at "either α=1,β=0 or α=0,β=1".

Leg 67's parenthetical that the `2/3` rung carries a smallness assumption on `‖θ₀‖_∞` is also
confirmed at source.

So the leg's claim (1) — *a published exponent by a similar name does exist, and it is `α+β=1`* —
is verified at primary source and is not overstated.

## Is the "not comparable" argument sound?

**Yes, and I found no more direct comparison it missed.** The published criticality is a property
of the *equation* (where its own scaling stops preserving the controlling norm; hence the
reduction to critical gSQG), indexed only by the dissipation powers. `s_c = 1/(2β_collapse)` is a
property of *one solution* — the rate at which dissipation on the Chen–Hou profile's collapsing
length scale overtakes that profile's driving — and depends on `c_l`, `c_ω`, which enter the
published ladder nowhere.

The decisive point is leg 67's own and it is correct: every published rung is a **one-sided
sufficient condition for global regularity**, hence an upper bound on any arrest threshold, never
an equality. An inequality bound and a claimed equality cannot be equated in principle.

Candidates I checked for a more direct route, both correctly excluded: Constantin–Vicol
`β > 2/(2+α)` needs thermal diffusion, and this repository's model is `θ`-inviscid (`β = 0`); the
2026 anisotropic-criticality paper yields blow-up *criteria*, conditional statements of the
category leg 67 already classified. The `β = 0` slice leg 67 compares on is the right slice for
`solver/fractional_boussinesq.py`'s model.

## How much does the negative actually establish? (the vacuity check)

Leg 67 says the ratio is "arithmetically vacuous — equals `1/β` identically by the definition of
`s_c`". **Verified, exactly.** With `α+β=1` evaluated at `β=0` the line is `α=1`; dividing
`α_equiv = 2s_c` by 1 returns `1/β = 0.3423999698147245` unchanged. The comparison recovers `β`
and nothing about the literature. Leg 67 is right, and right that this is *the* limit on what the
negative establishes — there is no external number in the comparison at all.

**One thing leg 67 does not say, and a rework should:** the vacuity extends to its "one real
external contact". The Hmidi–Keraani–Rousset margin factor `2.9206` is `1/α_equiv = β`, the same
identity inverted. Leg 67 hedges the contact correctly in words ("one-sided and weak — it would
pass for any `s_c < 0.5`", "recorded as a margin, not a validation") and never claims validation,
so nothing stated is false; but the margin *figure* is `β` restated and carries no external
information. Separately, since the solver derives the same `s_c` with dissipation on `θ`, the
`α=0` axis supplies more contacts of identical type and strength (HKR at `α=0,β=1`, Chae/Hou–Li
at `α=0,β=2`) — so the "one contact" is really several, all equally weak. Neither point changes
the gate's answer.

A third, purely bibliographic caveat: the rung "`(√1777−23)/12 ≈ 0.7981`" is internally
inconsistent (`/12` gives `1.5962`; `0.7981` is `/24`). **The typo is the source's**, and leg 67
transcribed it faithfully. But leg 67 then used it to "correct" its own Q5 query, which had
guessed `/24` and was arithmetically right. Nothing downstream depends on this rung.

## The false positive: independently reproduced

Leg 67 reports catching and discarding a `γ = 1/3` "published 1D critical dissipation exponent"
as a search-summary artefact. **I reproduced the artefact independently** — an unrelated
adversarial search of my own returned a summary asserting "the `C^γ` norm of the density `θ` with
`γ ≈ 1/3` is uniformly bounded up to the singularity time", attached to the Hou–Luo blowup
literature. That is precisely the conflation leg 67 diagnosed: `1/3` is the Hölder exponent of the
density in the self-similar result, silently re-badged as a dissipation exponent. Both abstracts
leg 67 says it checked to kill the lead (2601.02464, 2604.01868) were re-fetched and contain no
dissipation, no critical exponent and no `1/3`, as leg 67 states.

**The trap was real, the catch was correct, and logging rather than deleting it was the right
call.**

## Independent attempt to refute the negative

Two adversarial searches phrased against the leg's conclusion — one asking for blowup *persisting*
under fractional dissipation, one around the collapse rate — returned only the inviscid Chen–Hou /
Hou–Luo corpus on one side and the regularity corpus on the other, with nothing bridging them. **I
could not find a counterexample.** The absence leg 67 reports is corroborated, and its explanation
for why the absence is structural — `α_equiv = 0.3424` sits inside the supercritical regime
`α+β<1` that the survey itself calls "largely out of reach" — holds up.

## Conclusion

The gate's answer **NO**, for the quantity `solver/fractional_boussinesq.py` holds, survives
independent review. The exponent remains **internally-consistent-only**; no claim upgrade is
warranted and leg 67 correctly refrained from one. The `capabilities.py` annotation change leg 67
handed off (landed as `69b3139`) is a strictly stronger statement of the same negative and is
supported by what I verified.
