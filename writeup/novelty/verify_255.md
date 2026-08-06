# VERIFY 255 — post-landing review of Route-P1A (leg 255, commits `87ceb37` + `891ebaf`)

**Verdict: CONFIRMED, no gap.** All five claims check out against independent sources. One
**strengthening finding** on the most consequential judgement (the Leray clause) is recorded
below for leg 257 / the Decision Maker: the leg's verdict is right, but a **stronger and more
citable reason than the one it used is available in the same paper**, and a second reason
suggests the question leg 257 is scoped to ask may be *closed negatively* rather than open.

Independent of the leg's own runner and its summaries throughout (lesson 90): Breden–Chu was
re-extracted from the locally cached PDF (`Papers/2404.04054.pdf`, 3448 lines,
`pdftotext` md5 `944e134c462250c47b7236181832d5e2` — a different extraction than leg 245's, so
line numbers differ), and every cited arXiv row was re-fetched at source.

---

## 1. The Li–Zhou "killed by screen (iv)" verdict — AGREED, and it is stronger than the leg claims

**Transcription is exact.** Remark 40 sits at line 2750 of my extraction and reads verbatim, in
full — it is a **two-sentence remark**, nothing was elided:

> *"Remark 40. We deal with a one-dimensional example here for simplicity, but terms like
> (u · ∇)u could in principle also be handled in dimension d ∈ {2, 3}, as u ∈ H²(µ) is then
> still enough to guarantee that (u · ∇)u ∈ L²(µ) since u ∈ L∞(R^d)."*

This matches `REMARK_40["verbatim"]` in the runner character-for-character.

**The silence is real.** A full-text scan of the paper for `nonlocal`, `non-local`, `Leray`,
`pressure`, `incompressib`, `divergence-free`, and `Biot` returns **zero** relevant hits. All 11
`projection` hits are the spectral Galerkin projections `P_n`/`P_∞` onto Hermite–Laguerre
eigenspaces (lines 588, 612, 1196, 1606–1608, 2372, 2396, …) — unrelated to Leray. The leg did
not miss a passage.

**But "silence" understates the case, and this is the finding.** The leg reasons from *absence
of mention in Remark 40* — an argument from silence, which it honestly flags as "a strict
reading made deliberately." A **positive** exclusion is available one page into the same paper.
The work's governing equation, stated in the introduction as equation **(2)** (line ~98) and
carried as the standing form of the entire paper, is

> `Lu := −∆u − (x/2)·∇u = f(x, u, ∇u),  x ∈ R^d`

The nonlinearity is a **pointwise-local function of `x`, `u`, and `∇u`**. The Leray projection
`P[(u·∇)u](x)` depends on `u` over all of `R^d` and therefore **cannot be written in the form
`f(x, u, ∇u)` at all** — it is outside the paper's scope by the shape of equation (2), not
merely unmentioned in Remark 40. Remark 40 is an extension note *within* that local class
(it extends `d = 1 → d ∈ {2,3}` for a local term), not a statement about nonlocality.

**Assessment: the leg's verdict — Li–Zhou fails screen (iv) — stands, and should be re-grounded
on equation (2) rather than on Remark 40's silence.** This is not a correction to any number,
survivor, or gate answer; it is a stronger citation for the same conclusion. No repair made:
the leg is landed and the verdict is unchanged.

**Second, sharper point for leg 257 — the scoped question may be closed, not open.** The leg
writes that a future leg "could get it by *arguing the Leray projector into the reach*, which is
a real mathematical question," and hands that to leg 257 as the highest-value scoping target.
I would flag that this question looks **negatively resolved in the Breden–Chu space
specifically**, and leg 257 should test that before spending on it. The leg's own wording is
that Leray boundedness "does not follow from" the `H²(µ) ↪ L^∞` embedding — true but weak. The
stronger statement: the Leray projector is built from Riesz transforms (Calderón–Zygmund
operators), and CZ operators are bounded on a weighted `L²(w)` essentially only when `w` is a
Muckenhoupt `A_2` weight. Breden–Chu's weight is `µ = e^{|x|²/4}`, which grows **exponentially**
and is emphatically not `A_2` (`A_2` forces at most polynomial growth). So the expectation is
that the Leray projector is not merely un-established but **genuinely unbounded on `L²(µ)`** —
i.e. the obstruction is structural to the Gaussian-weighted space that makes the whole method
work, not a gap in Remark 40's exposition. I have not proven this here and state it as an
assessment, not a theorem; but leg 257 should check it **first**, because if it holds, the
"argue Leray into the reach" lane is dead on arrival and the leg's budget belongs elsewhere.
This makes the leg's own headline interpretation *more* true, not less: the nonlocality that
makes a model a fluid is excluded by the same weighted space that buys the method its
compactness.

---

## 2. The viscous-Burgers caution row is enforced, not asserted — CONFIRMED

`assert_probe_is_live()` (runner lines 511–535) is a real control, and runs on the actual table
before the gate (line 613). It is not vacuous on four independent counts:

* it fails the run if **no** row is killed, and separately if **every** row is killed (the
  yes-branch being unreachable by construction is caught);
* it requires **each of the four screens to kill at least one row** — no decorative screen;
* it requires **each of the four screens to PASS on at least one row** — no constant screen.
  These two together force both branches of every screen to be exercised;
* the Burgers clause itself reads `screen_verdicts(burgers)` — the verdicts are **derived from
  the row's evidence fields** by `screen_verdicts()` (line 437: `iv_bc_reach` is computed from
  `nonlocal_terms` and `principal_part_ok`), not stored. So the assertion genuinely fails if the
  evidence is edited into inconsistency; it is a guard, not a restatement.

`self_test()` additionally reaches **all four** distinct verdict codes on perturbed evidence
(`NO_MODEL_PASSES_ALL_FOUR`, `SURVIVOR_IS_FLUID_ADJACENT`, `SURVIVOR_ONLY_VACUOUS_TARGET`,
`SURVIVOR_NON_FLUID_NON_VACUOUS`), each against a pre-declared expectation. Both gate branches
are reachable.

---

## 3. Row spot-checks against sources — 4 of 4 CONFIRMED

Re-fetched independently at source, not read from the leg's summary:

| row | claim in the table | at source |
|---|---|---|
| `KS3D-NONEXPLICIT` (survivor) | `arXiv:2503.02263` builds infinitely many **non-explicit** self-similar profiles, `d = 3…9`, by matched asymptotics + Banach fixed point, **not** computer-assisted | **Confirmed** on all four counts, including the `2(d−2)/|x|²` far-field |
| `KS3D-EXPLICIT` (survivor) | `arXiv:2209.11206` Glogic–Schörkhuber: explicit (Brenner et al.) profile, nonlinear **radial** stability proved at `d = 3`, no interval arithmetic | **Confirmed**; semigroup/similarity-variable methods, purely analytic |
| `KS-NS-LI-ZHOU` (the fluid row) | `arXiv:2404.17228` proves 3D KS–Navier–Stokes blow-up; heart of proof is stability of an **explicit self-similar profile of Keller–Segel**; no certification apparatus | **Confirmed**, all three, quotes verbatim. The leg's honest sub-caveat — the self-similar object is the **chemotaxis** profile, the NS velocity is carried — is accurate and material |
| `KNS-FRACBURGERS` | `arXiv:0804.3549` Kiselev–Nazarov–Shterenberg: finite-time blow-up for `α < 1/2`, global existence + analyticity for `α ≥ 1/2` | **Confirmed**, both branches |

No misquoted source found in the sample.

---

## 4. Biernat–Donninger prior art — CONFIRMED on both halves

`arXiv:1610.09496` (Biernat & Donninger, Oct 2016) is at source *"Construction of a spectrally
stable self-similar blowup solution to the supercritical corotational harmonic map heat flow"*,
`R³ → S³`, with the abstract stating verbatim that *"a key ingredient is the use of interval
arithmetic: a rigorous computer-assisted method for estimating functions"* (a Mathematica
notebook is supplied). That is a Grade-A enclosure **on** a self-similar blow-up profile of a
dissipative (parabolic) object, non-fluid — leg 174's Grade-A definition, met.

**Genuinely unrecorded:** `solver/viscous_novelty.py` (12 arXiv entries in `PRECEDENTS`) and
`LITERATURE_CHECK.md` return **zero** hits for `1610.09496`, `Biernat`, `Donninger`, or
`harmonic`. The finding is real and eight years earlier than DF-CGL (2024), from a disjoint
author line. The leg correctly declined to edit either ledger (integration-owned) and staged the
row in `LEDGER_ADDITION_FOR_INTEGRATION` instead. **This remains an open action for
integration**, not for this review.

Bearing on the prize: this **adds** an occupant to the `(fluid=False, grade=A)` cell and leaves
`(fluid=True, grade=A)` **empty**, exactly as the leg says. It makes the non-fluid cell more
crowded — i.e. it lowers, not raises, the value of certifying a Keller–Segel profile.

---

## 5. Territory — CONFIRMED exact

`git diff --name-only 0a10572..891ebaf` is exactly the four declared files:
`experiments/journal/leg_255.md`, `experiments/p2_route_p1a_v1_census.py`,
`writeup/data/p2_route_p1a_v1_census.json`, `writeup/novelty/leg_255.md`. None of the five
shared ledgers touched; `plan_of_record.py` untouched.

## 6. Honesty discipline — CONFIRMED

No ban lifted or read as liftable; the ℓ¹-Fourier/radii-polynomial ban, the DSS ban and the gCLM
ban are each read and carried forward **as constraints on 3 flagged rows**, with no lift
requested. No construction attempted — construction is explicitly deferred to leg 257's ban-lift
scoping and the leg disclaims the authority. No L1→L4 link claimed to move, with the correct
reason given (a certificate on a non-fluid parabolic model would not move a link either). Clay
odds stated as ~0.05% behind Walls 1 and 2, Wall 2 in its corrected (time-dependent
singularity formation) form.

## 7. Reproducibility

The runner re-executes clean from a fresh checkout and regenerates
`writeup/data/p2_route_p1a_v1_census.json` **byte-identically** (empty `git diff`). All reported
magnitudes reproduce: 21 candidates, 2 survivors; kill counts (iv) 13, (iii) 6, (ii) 6, (i) 3;
sole-killer counts (iv) 7, (iii) 4, (ii) 1, (i) 0; cross-tab 9 / 2 / 7 / 4 / 3 / 3.

*Minor, non-blocking:* the narrative sentence "it kills **13 of 21** … and is the **sole** killer
on **7** — more than the other three combined (4 + 1 + 0 = 5)" compares one screen's *kill* count
against the others' *sole-kill* counts in the same breath. The arithmetic quoted is right and the
JSON carries both series separately, so nothing is wrong; the prose is just momentarily
ambiguous. Not worth a repair leg.

---

## Handoff line for leg 257 / the Decision Maker

> Leg 255's kill of Li–Zhou on screen (iv) is **correct and should be kept**, but re-ground it on
> Breden–Chu equation **(2)** (`Lu = f(x,u,∇u)`, a pointwise-local nonlinearity — the paper's
> standing scope) rather than on Remark 40's silence; the Leray projection is excluded by the
> *form* of (2), not merely unmentioned. And before scoping "can the Leray projector be argued
> into the reach", test the likely-negative answer first: Leray is a Calderón–Zygmund operator,
> `e^{|x|²/4}` is not a Muckenhoupt `A_2` weight, so boundedness on `L²(µ)` is expected to
> **fail**, which would close that lane rather than open it.
