# Route-M v1 — target selection: certify *what*, that isn't already done?

*Phase 2 / P2, leg 45. Figure: `writeup/figures/fig42_route_m_v1_targets.png`.
Code: `solver/target_selection.py`, `test_target_selection.py` (9/9);
`capabilities.py`, `test_capabilities.py` (5/5); `experiments/p2_route_m_v1_targets.py`
→ `writeup/data/p2_route_m_v1_targets.json`. Working notes: `PHASE2_P2_NOTES.md` §34.*

**The certification port has been aimed for twenty legs at a profile Chen–Hou certified
in 2022. This leg asks which objects are still uncertified and ranks six of them against
the one object where a proof of this kind was actually completed. Four are uncertified;
the top one costs 1.11e−3 of what the certified object costs — and its solver has been in
this repository, gated and unused, since 2026-07-26. The measured half of "reachable" (§3)
is still running as of this commit and is filled in from the JSON, not from memory. No link
of the L1→L4 chain moved. Clay odds unchanged at ~0.05%.**

---

## 0. What this leg is, in one paragraph

Route-J (leg 42) read the primary sources and deleted seven of twelve standing novelty
claims. That left a gap nobody had looked at: the port's *target*. `CLAY_ROADMAP.md` §2
says the realistic prize is a novel Tier-3 result on a model where blow-up is provable,
and the object the port has been aimed at is the one Chen–Hou proved. Closing a radii
polynomial there would demonstrate capability and produce no result. So: three questions
per candidate object — is it already certified, is it within interval-arithmetic reach,
what would certifying it contribute — sourced, ranked, and executable, because a
literature check that is not runnable decays at the rate of memory (lesson 68).

---

## 1. M1 — the ledger

Six candidate objects. `certified` is **not** "is blow-up known"; it is "is there a proof
of *this specific profile*", and an analytic proof counts harder than a computer-assisted
one, because an object proved by hand does not become more true when a computer re-proves
it.

| rank | object | certified? | dim | fields | mod | unknowns | / certified |
|---|---|---|---|---|---|---|---|
| 1 | **1D Hou–Luo, non-symmetric regular profile** (CHL Scenario 2) | **NO** | 1 | 2 | **3** | 1 203 | 1.11e−3 |
| 2 | **gCLM one-scale from degenerate data, `a>0`** (HTW26) | **NO** | 1 | 1 | 2 | 602 | 5.57e−4 |
| 3 | **2D Boussinesq, non-symmetric regular profile** (CHL §6.2) | **NO** | 2 | 2 | 3 | 720 003 | 6.67e−1 |
| 4 | **1D Hou–Luo, stability of the singular steady state** (CHL Conj 2.4) | **NO** | 1 | 2 | 2 | 1 202 | 1.11e−3 |
| 5 | 2D Boussinesq, Chen–Hou profile — *the port's current target* | **YES (CAP)** | 2 | 3 | 2 | 1 080 002 | 1.00 |
| 6 | 3D Navier–Stokes, backward self-similar profile | claimed, unusable | 3 | 3 | 2 | 6.48e8 | 6.0e2 |

Unknown counts are exact arithmetic — `fields × n^dim + modulation` at a common
per-direction `n = 600` — and the ratio is against **the one object where a proof of this
kind is known to have been completed**. That is the only honest calibration available; a
ratio ≤ 1 says cost is not the obstruction, and says nothing about conditioning.

**The exclusion list is the load-bearing half.** Seven objects are already proved, and
four of the seven were proved *analytically*, some of them after the computer-assisted
proof:

* **Chen–Hou**, arXiv:2210.07191 + Part II — the 2D Boussinesq profile. CAP.
* **Chen–Hou–Huang**, Ann. PDE 8 (2022) 24 — the Hou–Luo odd non-degenerate profile. CAP
  — **and then Huang–Qin–Wang–Wei, arXiv:2308.01528, proved it again by hand**, with
  monotonicity, convexity and far-field decay rates the CAP does not give.
* **Chen–Hou–Huang**, CPAM 74 (2021) 1282 — De Gregorio (`a=1`). CAP.
* **Huang–Qin–Wang–Wei**, arXiv:2305.05895 — gCLM smooth self-similar profiles for **all
  `a ≤ 1`**, analytic. This closes the entire smooth gCLM branch — the branch Routes D, E
  and F measured.
* **J. Chen**, arXiv:1908.09385 Thm 1.1 — dissipative gCLM near `a = 1/2`, analytic, no
  computer assistance anywhere in the paper.
* **Elgindi**, Ann. of Math. 194 (2021) 647 — 3D axisymmetric Euler, `C^{1,α}`, analytic.
* **Chen–Huang–Li**, arXiv:2604.01868 Thm 2.3 — *existence* of the singular Hou–Luo steady
  state, in the weak sense. Its **stability is Conjecture 2.4 and is open**, which is why
  the object still appears at rank 4.

### Why rank 1 is not rank 2

Rank 2 is the cheapest object on the list — a single scalar field, 602 unknowns — and it
is ranked second on purpose. The declared criterion is contribution first, cost last, and
`test_target_selection.py` gates that the uncertified ranking is **not** in cost order, so
a later re-sort by cost fails a test instead of passing silently.

What rank 1 buys, in Chen–Huang–Li's own words: in every existing proof of this kind "the
origin always acts as the source of stability". Their Scenario-2 profile has **no symmetry
point**, so the translation degree of freedom has to be carried by the certificate itself
— their formulation (2.9)/(4.1) adds a third modulation constant `c_r` for exactly this.
That is a methodological first, not another profile. It is also the shape leg 44 concluded
the 2D port needs: *border the system, do not project*.

---

## 2. M2 — what "within reach" means as a number

The radii polynomial, in the form this project has been writing since Route-D and in the
form Cadiot–Lessard–Nave state it (arXiv:2302.12877 Thm 4.6): with `Y₀ ≥ ‖AF(x)‖`,
`Z₁ ≥ ‖I − A DF(x)‖`, `Z₂(r) r ≥ ‖A(DF(v) − DF(x))‖`, a solution exists in `B_r(x)` when

    ½ Z₂ r² − (1 − Z₁) r + Y₀ < 0    and    Z₁ + Z₂ r < 1.

That has a root iff

    **Y₀ ≤ (1 − Z₁)² / (2 Z₂)**  — the *budget*.

`Z₁` and `Z₂` are properties of the operator and the space; `Y₀` is a property of how well
the profile is resolved. **Reach means: can the truncation be pushed until `Y₀` falls under
a budget the other two set.** That is a measurement, and it is why the M3 ladder below is
the leg's real work rather than a decoration on the ledger.

**Gated against a completed certificate.** CLN's Kawahara soliton (their Thm 6.6) publishes
`Y₀ ≤ 2.26e−14` and `r₀ = 2.27e−14`; our algebra returns their `r₀` from their `Y₀` with
relative error **0.0**, at an implied `Z₁ = 4.41e−3`. The budget boundary is checked by
bracketing on four `(Z₁, Z₂)` pairs — feasible at `0.999999999 ×` budget, infeasible at
`1.000000001 ×` — rather than evaluated at the boundary, where a strict inequality in
floating point is a coin flip.

### 2.1 The 3D Navier–Stokes claim, audited rather than assumed

arXiv:2604.09949 claims finite-time singularity for 3D Navier–Stokes on `T³` via a
computer-assisted Newton–Kantorovich validation. That is Q1 for the most consequential
target on the list, so it gets checked rather than waved at.

Its appendix D constants are `δ = 8.421739e−12`, `M = 482.6`, `K = 1.1e4`, and its
Corollary 10.4 closes on `2δMK ≈ 8.9e−5 < 1`. Kantorovich's hypothesis with `β = M`,
`η ≤ Mδ` and Lipschitz constant `K` is `M²Kδ ≤ ½` — in radii-polynomial form `Y₀ = Mδ`,
`Z₁ = 0`, `Z₂ = MK` — i.e. **one factor of `M` larger** than what is printed. Recomputed:
`2M²Kδ = 4.32e−2`.

**Both close.** The corrected form still has 23× of margin, and their `K` reproduces from
their own stated factor product to 2.2e−4. **The arithmetic is not where that manuscript
fails**, and the audit says so, because a check that reported "fails" here would be
reporting the wrong thing (lesson 76 — keep the negative construction in the artifact).

The reasons it cannot be used as a certification are therefore the ones that stand on
their own, and both are on the face of the document:

1. **No verification package exists.** Its own appendix F says the reproducibility package
   "is intended to contain" its contents, and appendix E says the source files "are not
   reproduced verbatim here because some previously uploaded files expired during the
   session". Constants asserted without a released check are not certified constants.
2. **The ansatz is the excluded one.** Their Thm 12.1 reconstructs an exactly *backward*
   self-similar solution, `Ω(r,z,t) = (T*−t)^{-1} Ω̄(r/√(T*−t), z/√(T*−t))`. That is the
   ansatz Nečas–Růžička–Šverák ruled out for nontrivial `L³` profiles and Tsai extended to
   locally finite energy — and the analytically weighted space `X` the manuscript works in
   implies far more decay than `L³` requires. Its reference list cites **Jia–Šverák on
   *forward* self-similar solutions, which exist**, and contains neither non-existence
   result.

So the ledger records the object as `CLAIMED_UNUSABLE`, not as certified and not as open,
and rank 6 is unchanged: everything to contribute, behind Wall 2, unreachable at 6.48e8
unknowns.

---

## 3. M3 — reachability, measured

> **⏳ PENDING — THE MEASUREMENT IS STILL RUNNING AS OF THIS COMMIT.**
> The refinement ladder for the named target (`experiments/p2_route_m_v1_targets.py`, M3)
> is deterministic and in flight; `writeup/data/p2_route_m_v1_targets.json` and **fig42**
> land with it, and this section is filled from that JSON and not from memory. **Nothing
> above depends on it:** M1 (the ledger), M2 (the budget algebra and the 3D-NS audit) and
> the gate verdict are complete and gated by `test_target_selection.py` 9/9. What M3 adds
> is the *measured* half of question (2) — whether the object our code converges to holds
> up as the grid is refined with the dissipation taken to zero, read as the ladder's
> DIRECTION (lesson 72) and paired with the same reading of Route-K's committed 2D ladder,
> where it went the other way (`1.671e−2 → 7.708e−2 → 2.667e−1` at `n_r = 300/450/600`:
> **2× finer, 16× worse**).


---

## 4. M4 — the same measurement on the object the port is aimed at

*(lands with M3 — see the pending note in section 3.)*

---

## 5. What this leg did NOT do

* **It did not certify anything.** No `Y₀`, no `Z₁`, no `Z₂` was computed for any
  candidate. M3 measures whether a fixed point is *there*, which is the prerequisite
  Route-K found missing on the 2D object — not whether a certificate closes around it.
* **It did not claim novelty.** Naming an object as uncertified is a statement about the
  literature listed in `Papers/MANIFEST.md` and read for this leg. `LITERATURE_CHECK.md`
  and `solver/literature_gates.py` remain the standing record.
* **It did not move the L1→L4 chain, and it does not touch Clay.** A better-chosen target
  is still a Tier-3 target. Walls 1 and 2 of `CLAY_ROADMAP.md` §7.3 are exactly where they
  were.
* **It did not re-open the port.** The port's target changes; the port's blocked steps (i)
  and (ii) and the unidentified near-null direction from leg 44 are unchanged and are the
  next leg.

---

## 6. The other finding, and it is about us

`solver/hl_rescaled.py::RescaledHLScenario2` — Chen–Huang–Li's three-constant bordered
formulation, with the gauge gated to 4.4e-16 and the contraction ratio reproduced to ~1% —
has been in this repository since **2026-07-26**, built as "the gCLM-ready gauge, validated
against a known answer" and then left. Nine legs later the port was aimed at a certified
object while the solver for an uncertified one sat unused, and this leg found it by
grepping for an arXiv number.

That is the same failure as the leg's headline, one level down: **the missing thing was an
index of what already exists.** `plan_of_record.py` answers *what is next*;
`PHASE2_P2_NOTES.md` answers *what happened*; nothing answered *what do we have*. So this
leg also ships `capabilities.py` — 35 solver modules, each with the object it holds, what
it computes, the strongest known-answer gate it passes **with the magnitude**, and its test
file — plus `test_capabilities.py`, which fails if a solver module exists without an entry,
if an entry points at a file that does not, or if a `validated` field is too thin to say
what was checked. Writing those five gates immediately turned up fourteen entries whose
validation claim was a shrug ("against dense norms"), and each was either filled in or
labelled *no independent published known answer*.

Banked lesson 68 applied to the inventory instead of to the literature.

---

## 7. Reproduction

```
bash Papers/fetch.sh                                     # ~30 s, PDFs gitignored
.venv/bin/python test_target_selection.py                # 9/9
.venv/bin/python test_capabilities.py                    # 5/5
.venv/bin/python test_line_hilbert.py                    # incl. the slope-operator gate
.venv/bin/python -u experiments/p2_route_m_v1_targets.py # ~45 min, deterministic
.venv/bin/python writeup/4_p2_lottery/p2_route_m_v1_evidence.py   # rebuilds fig42
.venv/bin/python capabilities.py hou-luo                 # the index, searched
```
