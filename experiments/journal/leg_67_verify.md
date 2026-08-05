# Leg 67 VERIFY — post-landing review of Route-FD v1 (literature leg)

**Date:** 2026-08-06. **Branch:** `verify/67-fd-review`. **Trigger:** (b), post-landing review.
**Verdict: PASS with two precision caveats.** No claim-bearing error found. Nothing repaired —
findings only.

Leg 67 commits reviewed: `54c8d8c` (novelty pass), `222efba` (query log + data + journal),
`69b3139` (Leg 0 ORCH, the `capabilities.py` annotation correction leg 67 handed off).

## 1. Primary source independently fetched and checked — CONFIRMED

arXiv:2606.03680 was fetched independently of leg 67's `Papers/` copy.

- Title and author list match exactly: Stefanov, Wu, Xu, Ye, *Global regularity of the 2D
  fractional Boussinesq equations with subcritical dissipation*, dissipation `(-Δ)^{α/2}u`,
  `(-Δ)^{β/2}θ`. The paper is real and is the paper leg 67 says it is.
- §1 quotes reproduced verbatim and confirmed word for word:
  - "the global regularity problem for (1.1) depends crucially on the value of α+β" and the
    three-regime classification subcritical `α+β>1` / critical `α+β=1` / supercritical `α+β<1`,
    attributed to Jiu–Miao–Wu–Zhang. **Confirmed.**
  - "In the special case α+β=1, the Boussinesq regularity problem boils down to the corresponding
    problem on the generalized surface quasi-geostrophic equation with critical dissipation."
    **Confirmed verbatim** — this is the vorticity-stream-equivalent half of the gate, and leg 67
    quotes it correctly.
  - "the global regularity problem for the supercritical regime remains largely out of reach,
    while substantial progress has been made in the critical and subcritical cases."
    **Confirmed verbatim.**
  - "how much dissipation is required to ensure global regularity?" **Confirmed verbatim.**
- The ladder on the `α+β=1` line is confirmed at all four rungs, in leg 67's order and with leg
  67's decimals: `α > (23−√145)/12 ≈ 0.9132`, `α > (√1777−23)/12 ≈ 0.7981`, `α > 10/13 ≈ 0.7692`,
  `α > 2/3`. Also confirmed: Constantin–Vicol `β > 2/(2+α), 0<α<1`; Chae and Hou–Li at
  `α=2,β=0` or `α=0,β=2`; Hmidi–Keraani–Rousset at "either α=1,β=0 or α=0,β=1".
- Leg 67's parenthetical that the `α > 2/3` rung is "under small `‖θ₀‖_∞`" is **confirmed**: §1
  reads "was established under the mild assumption that the L∞-norm of the initial temperature is
  small."

So part (1) of leg 67's answer — a published exponent by a similar name exists, and it is
`α+β=1` — is verified at primary source, including the gSQG reduction.

### Caveat A (source-fidelity, not claim-bearing)

`(√1777−23)/12 = 1.5962`, not `0.7981`. The value `0.7981` is `(√1777−23)/24`. The *paper itself*
prints "α>(√1777-23)/12≈0.7981", so leg 67 transcribed §1 faithfully and this is the source's own
typo — leg 67 is not at fault for the quote. But in Q5 of `writeup/novelty/leg_67.md` leg 67 goes
further and writes "Note the ladder is `(√1777−23)/12 ≈ 0.7981`, not `/24` as my query guessed",
i.e. it uses the source's typo to *correct its own query, which was arithmetically right*. The
same sentence is carried into the JSON at `queries[4].on_topic`. Nothing downstream depends on
this rung — it is context, not an input to any number leg 67 computes — so this is a fidelity
note for a future rework, not a defect in the result.

## 2. "Not comparable" — independently assessed, SOUND

I assessed the comparability argument on its own terms rather than accepting leg 67's framing.

The two quantities are genuinely different objects:

- The literature's criticality is a property of **the equation**: `α+β=1` is where the equation's
  own scaling stops preserving the controlling norm, which is why the case reduces to critical
  gSQG. It is indexed by nothing but the dissipation powers.
- This repository's `s_c = 1/(2β_collapse)` is a property of **one solution**: it compares the
  dissipation rate on the Chen–Hou profile's collapsing length scale against that profile's own
  driving rate. It is indexed by `c_l`, `c_ω`, which enter the published ladder nowhere.

Leg 67's second observation is the decisive one and it is correct: every published value on the
ladder is a **one-sided sufficient condition for global regularity**, so each is an upper bound on
any true arrest threshold, never an equality. Two quantities of which one is an inequality bound
and the other a claimed equality cannot be equated even in principle.

**I found no more direct comparison that leg 67 missed.** Two candidates were considered and both
fail for stated reasons: Constantin–Vicol `β > 2/(2+α)` is inapplicable because our solver
dissipates the vorticity with `θ` inviscid (`β=0`), which is outside its `β`-dominated hypothesis;
and the anisotropic critical paper (Applicable Analysis 2026) produces blow-up *criteria*, which
are conditional statements in the same category leg 67 already classified. The `β=0` slice, at
which leg 67 does its comparison, is the correct slice — I verified against
`solver/fractional_boussinesq.py`, whose model is `ω_t + u·∇ω = θ_x − ν(-Δ)^s ω`, `θ_t + u·∇θ = 0`.

### Caveat B (completeness, minor)

`solver/fractional_boussinesq.py`'s `relevance_exponent_buoyancy` derives the *same* `s_c` when the
dissipation is moved onto `θ` instead of `ω`. Leg 67 does not carry that through to the
literature comparison. If it had, the `α=0` axis would give two more external contacts of exactly
the same kind and the same strength — HKR at `α=0, β=1` and Chae/Hou–Li at `α=0, β=2` — each also
consistent, each also one-sided. This does not change the answer; it means the "one real external
contact" is really three or four contacts of one type, all equally weak.

## 3. The vacuity claim — VERIFIED, and it extends to the margin

Checked symbolically and numerically from `c_l = 3.00649898`, `c_ω = -1.02942516`:

    β         = -c_l/c_ω          = 2.9205610051341666
    s_c       = 1/(2β)            = 0.17119998490736224
    α_equiv   = 2 s_c             = 0.3423999698147245   = 1/β exactly
    |c_ω/c_l|                     = 0.3423999698147245   (identical, internal)
    α_equiv / 1                   = 0.3423999698147245
    gap in α  = 1 − α_equiv       = 0.6576000301852756

Leg 67's claim is **correct and it is an identity, not a coincidence**: the literature line
`α+β=1` evaluated at `β=0` is `α=1`, and dividing by 1 returns `α_equiv` unchanged, which is
`1/β` by the definition `s_c = 1/(2β)`. The ratio therefore recovers `β` and carries no
information about the literature at all. Leg 67 is right to call the check vacuous, and right that
this is the precise sense in which no external check is available. This is the correct and
important caveat on how little the negative result establishes, and leg 67 states it in both the
journal and the novelty file rather than burying it.

**The verifier's addition:** the vacuity extends one step further than leg 67 says. The
Hmidi–Keraani–Rousset "margin factor 2.9206" is `1/α_equiv = β` — *the same identity, inverted*.
So the number leg 67 reports as the margin of its "one real external contact" is the same
uninformative `β` it has just declared vacuous in the ratio. Leg 67 hedges correctly in words
("one-sided and weak — it would pass for any `s_c < 0.5`", "recorded as a margin, not a
validation") and never claims validation, so no statement is wrong. But a reader could take
"passes with margin factor 2.9206" as an independent quantitative margin, and it is not: the
margin figure is `β` restated. Recommended wording for any rework: state the margin as "passes;
the margin figure is `β` itself and carries no external information."

## 4. Hmidi–Keraani–Rousset — CONFIRMED accurate

§1 of 2606.03680 lists HKR at "either α=1,β=0 or α=0,β=1" for global regularity, which is exactly
how leg 67 characterizes it, and matches the known HKR results for the 2D Boussinesq system with
critical velocity dissipation and no thermal diffusion. The direction of the check is right: our
law predicts arrest for `α > 0.34240`, so at `α = 1` it predicts regularity, which is what HKR
prove — consistent, not a contradiction. The arithmetic `1/0.3423999698 = 2.9205610051` is
correct. Subject to Caveat B above (the margin is `β` restated), the citation is accurately
characterized and correctly labelled a margin rather than a validation.

## 5. The quartet — CONFIRMED, and the data is reproducible

All four files exist:
`experiments/p2_route_fd_v1_lit.py`, `writeup/data/p2_route_fd_v1_lit.json`,
`writeup/novelty/leg_67.md`, `experiments/journal/leg_67.md`.

`python3 experiments/p2_route_fd_v1_lit.py` runs clean (exit 0) and **rewrites
`writeup/data/p2_route_fd_v1_lit.json` byte-identically** — `git status` is clean afterwards. The
committed data is therefore reproducible from the committed script, and no solve is run: the
script's own banner reports "new solve runs: 0", matching the dispatch.

Every number appearing in prose in either markdown file was traced into the JSON:
`0.1711999849`, `2.9205610051`, `0.3423999698`, `0.6576000301852756`, `0.17120`, `0.34240`,
`2.9206`, `3.00649898`, `1.02942516`, `0.9132`, `0.7981`, `0.7692`, `10/13`, `2/3`, `0.8876`,
`0.7351`, `1777`, `145`, `3.188` — all present. **No orphan prose numbers.**

Bans: `plan_of_record.py` lines 716 and 786 do carry "re-measuring beta on the 2D object" and
"chasing the 2D near-null direction of leg 44". Leg 67 touches neither — the `β` it uses is the
closed-form collapse exponent `-c_l/c_ω` from published Chen–Hou constants, not leg 43's measured
growth rate, and the leg runs no solve at all. Ban check confirmed honest.

## 6. The discarded false positive (γ = 1/3) — INDEPENDENTLY REPRODUCED AND CONFIRMED CORRECT

This was spot-checked hardest, because a repository that catches its own false positives is worth
confirming does so correctly. It does.

- I fetched both abstracts leg 67 says it checked. arXiv:2601.02464 (Rampf–Kolluru, complex-time
  singular structure of the 1D Hou–Luo model): abstract confirmed to contain **no** fractional
  dissipation, **no** critical dissipation exponent, **no** `1/3`. arXiv:2604.01868 (Novel
  Self-similar Finite-time Blowups): abstract confirmed to contain **no** dissipation, **no**
  viscosity, **no** critical exponent, **no** `1/3`. Leg 67's account of what these two abstracts
  say is accurate.
- Better: I reproduced the false positive independently. An unrelated adversarial search of mine
  returned a summary asserting "the `C^γ` norm of the density `θ` with `γ ≈ 1/3` is uniformly
  bounded up to the singularity time" — attached to the Hou–Luo blowup literature. **This is
  exactly the conflation leg 67 diagnosed**: `1/3` is the Hölder exponent of the density in the
  Chen/Hou-Luo self-similar result, and a search summary re-badged it as a "critical dissipation
  exponent". Leg 67's diagnosis of the artefact's true origin is correct, and its decision to log
  rather than delete the retracted lead is the right call.

**The false-positive catch is sound.** It was a genuine trap, leg 67 walked into it, detected it
by going to primary source, and recorded the detection.

## 7. Independent test of the negative

I ran two adversarial searches designed to break leg 67's "NO" — one phrased as *blowup persisting
under* dissipation rather than regularity, one phrased around the collapse rate. Both returned
only the inviscid Chen–Hou/Hou–Luo corpus on one side and the regularity corpus (2606.03680, the
anisotropic-criteria paper, horizontal/vertical-dissipation papers) on the other, with no paper
bridging them. **I could not find a counterexample.** The gate's answer NO, for the quantity on
file, stands after an independent attempt to refute it.

## Bottom line

Leg 67 is a well-executed negative. Its primary source is real and quoted accurately, its central
distinction is sound, its arithmetic is exact, its self-declared vacuity caveat is correct and
is the honest thing to have said, its false positive was a real trap correctly caught, and its
data reproduces byte-identically from its own script. Two precision caveats (A: an inherited
source typo used to "correct" a correct query; B: the HKR margin figure is the same vacuous
identity `β`, and the `α=0` axis supplies more contacts of the same weak type). Neither changes
the gate's answer or any claim. **No rework required; caveats are for the record.**
