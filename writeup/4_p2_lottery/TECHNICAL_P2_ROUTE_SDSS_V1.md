# Route-SDSS v1 (leg 313) — does leg 260's substantive obstruction survive a SEEDED search?

**Gate, in its pre-committed wording:**

> **Does leg 260's substantive obstruction survive seeding, with the (a)/(b)/(c) triple
> answered either way?**
>
> **NO.** Leg 260's substantive obstruction — verbatim, *"Entry B's defining adjective
> UNSEEDED is incompatible with its object's only function space"* — **holds in exactly one
> named realization: a finite-box, finite-energy spectral trawl measured in the unweighted
> `L²(dy)` norm on `R³`.** It does not hold in the space leg 260's **own** answer (a) names
> (weighted `L²(ρ)`, `ρ = (1+|y|)^{-s}`, `s > 1`; crossing measured here at exactly `s = 1`),
> and it does not hold in the algebraically compactified variable `X = |y|/(1+|y|)` that the
> one **demonstrated** seeded method actually uses, where the Type-I profile is the **exact
> linear zero `(1-X)`** with finite norm `√(1/3) = 0.577350`. All four of leg 260 §3.4's
> reasons dissolve under seeding, including the two leg 260 itself named as *"the finding"*.
>
> **A different obstruction — not leg 260's, and not a price either — stands in its place,
> and is measured here.** The (a)/(b)/(c) triple is answered in §§1–3.

**This is the escalation branch. This leg does not lift the ban, and did not touch
`plan_of_record.py`.** The branch is `leg/313-sdss-v1`, parked, not merged to `main`. The
ruling is the user's. The 3D-solver amendment keys off this same answer and is also the
user's to action, not this leg's.

**Novelty pass:** `writeup/novelty/leg_313.md`, committed at `af3b7e0` **before** the runner
existed. **Runner:** `experiments/p2_route_sdss_v1_scoping.py`. **Ledger:**
`writeup/data/p2_route_sdss_v1.json`, **30/30 self-tests pass**. **Figure: fig76**
(`writeup/figures/fig76_route_sdss_v1.png`, rebuilt from the JSON alone by
`experiments/p2_route_sdss_v1_evidence.py`, registered in `writeup/build_figures.py`).

**Scope: paper scoping only. No construction, no search run.** No solver was built, run, read
into, or edited. Everything below is quadrature, a Chebyshev transform of a closed form, and
arithmetic — exactly the scope leg 260's own scoping runner operated in.

**No link of the L1→L4 chain moved. Clay odds stay ~0.05%.** Nothing here is movement toward
Clay. Answering a scoping question is choosing what not to try.

---

## 0. The named mechanism

**THE COMPACTIFICATION TRANSPOSITION — the log-periodic block's regularity defect is an
invariant of the entrance, not a property of the domain's far end. You can move it from
infinity to a boundary point; you cannot delete it.**

Leg 260's obstruction is a statement about a *norm on an unbounded domain*. Seeding lets the
search work in a compactified variable, where that norm is finite — so the obstruction goes.
But the **same** compactification that makes the norm finite carries the far-field block

    r^{-1+iκ}   ↦   (1-X)^{1-iκ},        X = |y|/(1+|y|)

and `(1-X)^{1-iκ}` is the **identical functional form** to clause (a)'s recorded gCLM
difficulty `X^{1-iy}` (`PHASE2_P2_NOTES` §26 / Route-E §4.1) — a fractional power at a
boundary point — now sitting at `X = 1` instead of `X = 0`. The difficulty is conserved under
the map. **It is not about the seed, which is why seeding does not touch it.**

Measured consequence: the compactified block's Chebyshev coefficients decay **algebraically**
at fitted rate `p = 3.000`, not geometrically. See §1.2 for the cost that buys.

---

## 1. (a) THE FUNCTION SPACE — answered

### 1.1 The same object, three verdicts

The object is the Type-I profile `|U(y)| ≤ C/(1+|y|)` on `R³` (Chae–Wolf `arXiv:1610.09464`
Thm 1.1, carried from leg 253 via leg 260 — **not re-derived here**). Shell integrals
`∫_R^{2R} / ∫_{R/2}^{R}` started at `R = 1e4`, deep in the asymptotic regime, which is leg
260's own hard-won lesson and is reused rather than rediscovered.

| space | shell ratio | verdict |
|---|---|---|
| unweighted `L²(dy)` | **2.000277** | **DIVERGES** — leg 260 §3.4 reason 2 |
| weighted `L²(ρ)`, `s = 0.9` | 1.071997 | diverges |
| weighted `L²(ρ)`, `s = 1.0` | 1.000216 | **the crossing** |
| weighted `L²(ρ)`, `s = 1.1` | 0.933242 | **FINITE** |
| weighted `L²(ρ)`, `s = 1.5` | 0.707 | finite |
| compactified `X = |y|/(1+|y|)` | — | **FINITE**, `‖U‖_{L²(dX)} = √(1/3) = 0.577350` |

Every weighted row agrees with the closed form `2^{1-s}` to `< 1e-3` relative, and the
residual is **explained**, not tolerated: it is the `O((2+s)ln2 / R)` correction from using
the faithful envelope `(1+r)^{-1}` rather than the pure power `r^{-1}`.

**Positive control against a banked number.** On leg 260's **own** integrand (the pure power
`|U| = r^{-1}`, whose closed form is `2^{3-p}`) this leg's quadrature reproduces leg 260's
banked divergent `p = 2` row **2.000035** to `< 1e-4` (measured 2.000000). The `1.2e-4` gap
between that and this leg's 2.000277 is the envelope, not an error, and is separated on
purpose so the control tests the instrument rather than flattering it.

**The compactified row is the operative one, and it is exact.** Under `X = |y|/(1+|y|)` the
Type-I envelope `(1+r)^{-1}` becomes **exactly `(1-X)`** — a linear zero at the boundary,
representable by any polynomial basis, with `L²(dX)` norm `√(1/3)`, matched to `< 1e-6`.
**This is not a convenience of this leg's choosing:** it is the discretisation the one
demonstrated seeded method actually uses — Hou `arXiv:2405.10916` computes *"in a transformed
domain on a uniform mesh, which maps back to a highly adaptive physical mesh."*

**So leg 260 §3.4 reason 2 — *"a finite-box spectral method represents finite-energy states;
a trawl cannot recur near an object outside its own space"* — is a true statement about a
finite-energy box, and false about the space the seeded entrance runs in.** Its realization is
named, per lesson 91: **the unweighted `L²(dy)` finite-box spectral trawl.**

### 1.2 Clause (a)'s recorded difficulty, carried — and it survives, transposed

The ban's lift clause (machine-read from `plan_of_record.BANNED` at run time, never
transcribed — self-tests S1.10/S1.12) requires carrying §26/§4.1's difficulty: building
blocks of **limited regularity at the origin** (`X^{1-iy}`), and **the viscous gCLM band
absent entirely** (`max Re = -1e-13` at `mu = 0.05`).

Both are carried, and they part company:

* **The viscous band's absence does not transfer.** It is a gCLM statement, and clause (b)
  of the ban's own text says so (*"Nothing about NS. gCLM's scaling structure is not NS's"*).
  Leg 260 §1.1 already explained the mechanism with its crossover formula — the gCLM band
  sits where dissipation wins, the NS band where the rescaling drift wins by `r²`. **This leg
  transcribes that and re-derives none of it.**
* **The limited-regularity difficulty DOES transfer — by transposition, and it is the finding
  of §0.** Under the same compactification, `r^{-1+iκ} ↦ (1-X)^{1-iκ}`.

Measured cost of that transposition — Chebyshev coefficients on `[0,1]`, `N = 2^20`:

| `κ` | fitted decay rate `p` | modes for `1e-6` relative truncation |
|---|---|---|
| smooth control (entire, asymmetric) | **geometric** | **10** |
| 0 (control) | terminates exactly | 2 |
| 1 | 3.000 | **823** |
| 2 | 3.000 | 1482 |
| 5 | 2.999 | 3564 |
| 10 | 2.994 | 7086 |
| 20 | 2.977 | **14149** |

Cost law across the measured rows: **`n(κ) ≈ 791 · κ^0.954`**, max relative residual **3.9%** —
i.e. **essentially linear in the log-periodic frequency**. Reported as a shape, not an
endpoint (lesson 72). At the cheapest `κ ≠ 0` row the separation from the smooth control is
**82.3×** at the same tolerance on the same instrument.

**Controls, both directions.**
* The `κ = 0` row is a control that **can come out differently**: at `κ = 0` the exponent
  `1-iκ` is `1`, so `(1-X)^1` is a **polynomial** and the defect must vanish — and it does,
  `max|a_n| = 2.1e-17` for `n ≥ 3`. Had it not terminated, the measurement below would have
  been an artifact of the transform rather than a property of the object.
* The smooth positive control is entire and **asymmetric**. This matters, and the failure is
  kept in the artifact: the first draft used `exp(-8(X-1/2)²)`, which is **even** about the
  midpoint, so **all** its odd Chebyshev coefficients vanish identically (`max` odd `|a_n| =
  4.2e-17`) and the "first coefficient below tolerance" test reported `n = 1` for a **symmetry
  reason having nothing to do with smoothness** — lesson 90 exactly, a control that could not
  come out differently. Replaced, and the criterion strengthened to "last index at or above
  tolerance", which no symmetry can fake.

**A resolution correction, kept in the artifact.** The first draft ran at `N = 2^14`. Under an
8× refinement the `κ = 20` cost moved **29.8%** (10841 → 14073) and the `1e-8` column
**saturated against the array** (`n = 16332` of `N = 16384`). Those numbers were measuring the
array, not the object. The runner now works at `N = 2^20` and carries a three-level study: the
`1e-6` rows are stable to **≤ 0.5%** against the 8×-coarser level. **The `1e-8` column is
withdrawn and is not quoted anywhere.**

**Extrapolation, explicitly not an NS number.** At gCLM's leading `|Im| = 430.35` (Route-I)
the cost law gives **257,466 modes**. **Clause (b) forbids importing gCLM's frequency into
NS**, and this row is reported only to price an import that is *not* licensed. **The NS
log-periodic frequency is unknown — it is an output of the very search being scoped.**

---

## 2. (b) THE OBJECT — answered, and the new obstruction is here

**All three ban reasons hold only in gCLM while Phase 0's target is NS.** Machine-confirmed
from the ban's own lift text (S1.11): the clause contrasts gCLM with NS in as many words. That
half of (b) is exactly as leg 254 and leg 260 recorded it, and it is unchanged.

**The object under seeding** is leg 251's `NS3D-DSS-NONAXI-LAMBDA-LARGE`: 3D incompressible
NS, **non-axisymmetric** backward DSS, `λ` significantly larger than 1, profile outside
`L^∞_t L³` — as a search target, a **periodic orbit of the dynamically rescaled flow with
period `T = 2 log λ`**. The novelty pass re-located that equivalence from an independent
published source: Chae `arXiv:1306.0305` defines the asymptotically-DSS object as a solenoidal
`V̄(y,s)` with `V̄(y,s) = V̄(y,s+S₀)`, `S₀ ≠ 0`. **DSS is time-periodicity of the rescaled
field**, published, not this repository's coinage.

**The seeded entrance has been operated — on a neighbour object.** Hou `arXiv:2405.10916`
does all three things Route-SDSS's entrance needs: it **seeds** (*"the initial condition for
the dynamic rescaling formulation is obtained from a late-stage adaptive-mesh solution,
rescaled via parabolic scaling invariance with a soft far-field cut-off"*), it works on a
**transformed unbounded domain** rather than a finite-energy box, and it **continues** in
viscosity `ν₀`. It also names the obstruction seeding exists to defeat — **scaling
instability**, which means a time-marching method *"can only get close to the potential
blowup without reaching arbitrarily near the blowup time."*

**And this is where the new obstruction is.** That candidate is on the **wrong side of the
screen**, three times over:

1. **Axisymmetric.** Leg 253's composition (Chae–Wolf Thm 1.1 with the axisymmetric Type-I
   exclusion, labelled there as that leg's own inference) kills axisymmetric DSS outright.
2. **Generalized, not NS.** Solution-dependent viscosity, effective dimension **≈ 3.188**
   (reported as apparently → 3 as background viscosity falls). Phase 0's target is NS.
3. **Stationary, not time-periodic.** It is a *nearly self-similar* profile — a fixed point of
   the rescaled flow — not a DSS orbit.

And the novelty pass's located gap closes the alternative: across every query and spelling
variant, **no source computes a genuinely discretely self-similar (time-periodic in `s`)
blow-up profile for Navier–Stokes numerically.** The genuinely time-periodic computations that
exist are **forward** DSS (Tsai) or **other equations** (NLS log-log, Keller–Segel), where
unstable modes are removed using symmetries and the spectral analysis of a **compact**
linearised operator about an **explicit ground state** — *"a luxury unavailable for NSE, since
there is no explicit ground state and the linearized operator is not compact."*

> **THE SEED SET FOR THE SCREENED OBJECT IS EMPTY.** No published numerical DSS candidate for
> 3D NS survives the NRS/Tsai + axisymmetric screen, so a search "seeded from a known
> numerical DSS candidate" has, today, nothing to be seeded from.

**This is a new obstruction, it is not leg 260's, and it is not a price — but it is an
availability fact, not an impossibility.** Two published recipes manufacture a seed rather
than find one: Hou's own `ν₀`-continuation plan (drive `c_l(ν₀) → 1/2`, `n(ν₀) → 3`), and
Chen `arXiv:2605.15149` (14 May 2026), whose rigorous construction runs a **fixed-point
argument around a numerically constructed approximate profile**. **Manufacturing the seed is
therefore the first item of the price, not a reason the route is closed** — and saying which
of those it is, is the user's ruling, not this leg's.

**Wall 2, explicitly.** The screened object is **non-axisymmetric 3D with no symmetry
reduction available**. That is squarely on the far side of Wall 2, and this leg claims nothing
otherwise.

---

## 3. (c) THE PRICE — answered, with a correction to leg 260

### 3.1 The build floor ROSE, and leg 260 told us to check

`capabilities.py` is read **live** by the runner, never hardcoded.

| | modules indexed | legs | legs/module | five-module floor |
|---|---|---|---|---|
| leg 260 | 48 | 260 | 5.42 | **27** |
| **leg 313** | **48** | **313** | **6.52** | **≈ 33** (32.6) |

Leg 260 wrote that the floor *"should be re-read, not cited"* and predicted it would **fall**
as this repository delivers modules. **53 legs later the module count is unchanged at 48, so
the floor ROSE from 27 to ≈33.** Leg 260's instruction was right and its prediction's
direction was wrong; both are recorded. The five must-build modules are unchanged from leg
260 §3.1 (3D NS in similarity variables; 3D Leray/Biot–Savart; an unbounded-domain
discretisation carrying an algebraic far field with log-periodic oscillation; a periodic-orbit
search; a phase/gauge condition). **The standing grep-first ban is honoured: 0 modules hold a
periodic-orbit search, 0 hold a 3D velocity field, 0 hold a Leray projection.**

**Seeding does change one of the five in kind, though not in count.** The periodic-orbit
search stops being a global trawl and becomes a **local Newton–Krylov / multiple-shooting
continuation** — 22-year-old published machinery at NS discretisation dimension `O(10⁴)`
(Sánchez–Net–García-Archilla–Simó, *J. Comput. Phys.* **201** (2004) 13–33), whose own
guidance is that **good initial conditions matter most** for exactly this task. It is still
absent from this tree; it is no longer unprecedented.

### 3.2 The resolution demand, now measured rather than assumed

This is the contribution leg 260 could not make, because it had not measured the transposed
block.

| | value |
|---|---|
| radial modes for `1e-6`, worst measured `κ = 20` | **14,149** |
| smooth control at the same tolerance | 10 |
| **radial resolution penalty** | **1414.9×** |
| DOF, `128² × 14149 × 2` | **4.64e8** |
| vs a uniform `128³ × 2 = 4.19e6` | **110.5×** |
| vs Phase 1's viscous rung (`2 × 10⁴` DOF, ≈14 h single CPU) | **23,182×** |

The deliverables remain incomparable in kind, exactly as leg 260 said: Phase 1's rung outputs
a **Grade-A certificate** from a **1D ODE** enclosure; this outputs a **float candidate** on
the far side of Wall 2.

### 3.3 What leg 260 said "resists" no longer resists

Leg 260's §3.4 reason 4 — *"a time-boxed negative would not be reportable"*, because a cold
search over ~4.2e6 dimensions has **no coverage metric** — is a property of a cold search. A
**seeded** Newton–Krylov continuation reports a **residual**, a **condition number**, and a
**continuation arclength before failure**: its failure **is** a magnitude, in this
repository's own required form. **So the search step becomes costable in precisely the sense
leg 260 found missing** — which is the sense its gate's word "actionable" required.

---

## 4. All four of leg 260 §3.4's reasons, under seeding

| | leg 260's reason | under seeding |
|---|---|---|
| 1 | the only demonstrated unseeded method (recurrent-flow extraction) needs an **ergodically visited** trajectory, which the rescaled flow does not supply | **dissolves** — seeding removes the need for an ergodic substrate, and a demonstrated *seeded* method exists (`arXiv:2405.10916`) |
| 2 | **the target is not in the trawl's state space** (infinite energy in the similarity variable) | **realization-scoped** — true in the unweighted-`L²` finite box, false in (a)'s own weighted space (crossing at `s = 1`) and in the compactified variable (exact linear zero, norm `√(1/3)`) |
| 3 | **representing it requires `λ`** — *"impose it and the search is seeded"* | **dissolves by construction** — the antecedent **is** seeding. Hou imposes precisely this, as a *"soft far-field cut-off"* |
| 4 | a time-boxed negative would not be reportable (no coverage metric) | **dissolves** — a seeded continuation's failure is a residual, i.e. a magnitude |

**Leg 260 named reasons 2 and 3 as *"the finding"*.** Both are the ones that dissolve most
cleanly. That is the gate's answer.

---

## 5. A ban-scope observation — REPORTED, NOT ACTED ON

Machine-read from `plan_of_record.BANNED` at run time (S1.4–S1.6, S1.13):

* **Entry A** bans *"any attempt to obtain a DSS orbit by **BIFURCATION OFF A FIXED POINT** of
  a rescaled flow (Hopf or otherwise), inviscid or viscous."*
* **Entry B**'s object clause is *"a **GLOBAL** periodic-orbit search of a rescaled flow with
  **no fixed point nearby to seed it**."*
* **Neither entry names a search seeded from a known numerical DSS candidate.**

A seeded search of that kind is not a bifurcation off a fixed point (Entry A's object) and is
not a search with no seed (Entry B's object). **Whether Entry B's substantive basis was
intended to reach it is a question about the ban's wording, and a wording question is not a
judgement an agent may make** — precisely the shape of leg 304's escalation over Cadiot.

**THE BAN STANDS IN FORCE, UNCHANGED, AND BINDS EVERY LEG. This leg has no authority over
`plan_of_record.py`, did not touch it, and does not lift, re-pose, or weaken anything.** The
observation is handed to the user with the (a)/(b)/(c) triple attached, which is what the
dispatched no-branch requires.

---

## 6. Honest ceiling

* **A dissolved obstruction is not a discovery, and it is not permission.** What this leg
  establishes is that leg 260's stated reason is scoped to a realization it did not name, and
  that a **different** obstruction — an empty seed set for the screened object — now occupies
  the position. Neither fact opens anything on its own.
* **A THIRD obstruction, and the only one of the three that is a theorem.** Located on this
  leg's MF3 re-audit of its own novelty pass (`writeup/novelty/leg_313.md` §8a): **Chae–Tsai
  prove nonexistence for DSS solutions with time-periodic `V`** under decay assumptions on the
  vorticity profile `Ω = ∇×V` — unique-continuation type, with `S₀ > 0` the temporal period
  and conclusion `V ≡ 0`. That is **precisely the object of §2**, met in the nonexistence
  direction. The same rigidity line for Euler is Xue `arXiv:1408.6619` and J. Nonlinear Sci.
  `10.1007/s00332-023-09975-1`; `arXiv:2602.17570` (2026) argues separately that producing NS
  singularities via Euler self-similar solutions must fail in the case it analyses.
  **Reported at summary level only.** Whether the decay hypothesis on `Ω` excludes the
  screened object or merely a decaying subclass **is not known to this leg and is not
  guessed**, and no claim in §§1–4 leans on it; a follow-up leg must read Chae–Tsai at full
  text. It does not alter the gate — it is not leg 260's argument — but **any ruling on this
  route should be made with it in view**, because it is the one item here that could close the
  route outright rather than merely price it.
* **§0's transposition is arithmetic about a closed form, not a theorem about NS.** That
  `r^{-1+iκ} ↦ (1-X)^{1-iκ}` is exact; that the NS far field genuinely carries a log-periodic
  block with a particular `κ` is **hypothesis**, and `κ` itself is unknown. The measured cost
  table is conditional on that structure, and every extrapolation beyond `κ = 20` is labelled.
* **The seed-set-is-empty finding rests on a literature search, not on a theorem.** It is a
  located gap at abstract/summary level; **no external PDF was read at full text this leg**,
  and `arXiv:2405.10916` is the one a follow-up leg should read fully. The (b) answer depends
  only on that paper's object being **axisymmetric**, which is in its title.
* **The `1e-8` column was withdrawn**, and the `N = 2^14` numbers that appeared in this leg's
  own first draft (κ=20 → 10841) are superseded by the converged `N = 2^20` ones (14149).
  Both are recorded rather than quietly replaced.
* **Two of this leg's own controls were defective on the first pass** — a symmetric smooth
  control and a tautological comparison — and both are described in §1.2 with their repairs.
  Lesson 90 caught them; they are kept in the artifact.
* **Dependencies live on parked branches** (legs 251, 253, 257, 260) and are carried with
  locators and parked status stated, never re-derived.
* **No compute beyond quadrature, one Chebyshev transform, and arithmetic. No solver built,
  run, read into, or edited. No search run.**
* **Clay odds ~0.05%, zero links of L1→L4 moved, Walls 1 and 2 both stand.**
