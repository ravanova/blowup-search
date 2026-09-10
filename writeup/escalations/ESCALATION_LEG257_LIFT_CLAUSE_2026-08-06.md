# ESCALATION — leg 257: the stage-V lift clause is MET ON PAPER, and the route closes anyway

**Raised** 2026-08-06 by leg 257 (Route-P1C), which escalated rather than landed.
**Carrier until 2026-09-10:** GitHub PR **#19**, now CLOSED UNMERGED. The work is preserved on the
pushed branch — see §5. Closing the PR retired the *carrier*, not the question.
**Status: OPEN. RECORDED, NOT RULED.** This is **row 5** of the open-escalations table in
`reports/ORCH_STATE.md` — *"the leg-257 lift-clause defect … Recorded, not ruled, and still
EXEMPLAR-FREE."* Lifting or weakening a ban other than via its recorded lift condition is
`ORCHESTRATION.md` §8 escalation 2. **Distinct from row 4** (`ESCALATION_BAN_WORDING_2026-08-13.md`),
which is about applying a recorded edit; this one is about whether the clause is defective at all.

---

## 1. The defect, in one sentence

The stage-V ban's lift clause asks for **a namable fourth function space with its own scoping leg
establishing non-subjection to the named death mechanisms** — leg 257 supplied exactly that, and the
route then died of a **fourth** obstruction that is not on the ban's list. **A lift clause that can
be satisfied in full by a route that is already closed is not testing what it was written to test.**

## 2. The lift clause, satisfied on paper

**The space:** `H²(µ)`, `µ = Γ(d/2)(2√π)^{−d}e^{|x|²/4}`, Hermite–Laguerre spherical eigenbasis of
`L = −Δ − (x/2)·∇` (Breden–Chu, Definition 5, line 299). Never tried here — leg 163 found `solver/`
has **no `L²` or Sobolev norm object at all**. Novelty pass returns **n = 1**, the parent itself.

**Its own scoping leg, mechanism by mechanism, each with its own locator and none by analogy:**

| mechanism | transfers? | why not |
|---|---|---|
| **M1** leg 54's `Z₁` block-coupling | **No** | Evaded *at the hypothesis*: `L⁻¹` compact via a genuine Poincaré inequality on `ℝ^d`; the unbounded part `L` is exactly diagonal — a multiplier, where leg 51 found `ℓ¹_w`'s was a shift. No border anywhere in BC, so the precondition is absent. |
| **M2** leg 56's `(H,D)` consistency defect | **No** | Needs an interpolatory discretisation of a nonlocal operator; BC have neither. The defect is **identically zero**, not small. |
| **M3** legs 163/176's `a=0` exactness cap | **No** | **Negation demonstrated**: Thm 2 encloses a non-radial profile nobody had inverted in closed form. |

`Z₁` where `< 1` is needed: **BC 0.065136** vs leg 54's **8.9591** and leg 176's **140.72**.

## 3. The fourth obstruction, which is what actually closes the route

**The Leray projection leaves `L²(µ)`. Measured, not argued.** Witness `U = curl(e^{−|x|²}e₃)`,
divergence-free exactly and Gaussian. `P[(U·∇)U]` has an algebraic `|x|⁻⁴` tail — fitted exponent of
`v` **−3.000000**, multipole ratio **1.000000** at `r = 10/20/40/80`, `T = ∫|U|² = 3.937402486`
stable to **12 digits** over three quadratures — while the Gaussian control `|(U·∇)U|` underflows to
**exactly 0.0** at every radius. **The coefficient IS the energy, so it cannot vanish.** Hence
`P[(U·∇)U] ∉ L²(µ)` for any nonzero divergence-free `U ∈ H²(µ)`, and `F(U) = U − L⁻¹P(…)` is **not
well-defined** on `H²(µ)`. Holds in **d = 2 and d = 3, self-similar or not.**

**Both obvious repairs re-open a closed door:** bordering the space re-introduces exactly leg 54's
M1; swapping to an algebraic weight destroys the Poincaré inequality — which is **the single root of
all three evasions** in §2. The three are not independent evidence.

## 4. The question, stated so it can be answered Y or N

**Q. Is the leg-257 lift clause defective as recorded — Y or N?**

- **Y** means the clause needs re-wording before any future route can be judged against it: as
  written it certifies "not subject to the three named mechanisms" when what the ban is protecting
  against is "subject to *any* mechanism of that kind". The re-wording is the user's, not a
  measurement, so it cannot be supplied by a leg.
- **N** leaves the clause standing as written, with leg 257 on record as having met it and closed
  anyway — **and the row stays EXEMPLAR-FREE**, which is what it has been since 2026-08-06.

**What is NOT asked here:** no ban is being lifted, and leg 257 did not take the lift. The journal is
explicit: *"the lift is the user's signature, not this leg's"*, `plan_of_record.py` byte-identical to
`origin/main`'s.

## 5. Where the work is

Branch **`leg/257-p1c-v1`**, head **`8caf8d9d48addd5fcedafbe95f341ab02f1eb6f4`**, 4 commits, never
merged to `main`. Four files, 2,125 insertions: `experiments/journal/leg_257.md`,
`experiments/p2_route_p1c_v1_reach.py`, `writeup/data/p2_route_p1c_v1_reach.json`,
`writeup/novelty/leg_257.md` (committed at `2e84d2c`, before a line of the runner existed).

`arXiv:2404.04054` re-fetched at primary source, **md5 `ff7a34b776bfe5edf97397e5eabdbb7a`, 2060
lines — matching leg 245's pin BIT-FOR-BIT.**

## 6. Cross-checks and what the leg withdrew

Leg 255 (P1A) killed its one fluid-adjacent candidate on **the same Leray-projection clause** from a
21-model census, by a different instrument and not coordinated. Leg 257 **agrees with its kill and
withdraws its concession** that a later leg "could get it by *arguing* the Leray clause" — §3 shows
it cannot. Of leg 255's verifier's two arguments, leg 257 **confirms the eq-(2) locality argument
independently** and **rejects the Muckenhoupt A₂ argument as an inference** — A₂ is sufficient, not
necessary, so "the standard condition fails" ≠ "the operator is unbounded". It does not need to be
relied on: §3 exhibits the failure.

## 7. Two things carried, not resolved

- `‖u‖_{L³(ℝ³)} ≤ 3.419108·‖u‖_{H²(µ)}` puts `H²(µ)` inside the NRS/Tsai screen. **Ceiling:
  NRS/Tsai is not this leg's and not novel; leg 253 owns its hypothesis boundary, and if it moves
  this must be re-derived.**
- Cost, had it been open: the wall sits between `‖Ū‖_∞ = 5` (**0.36 TB**) and `10` (**661 TB**).

**No link of the L1→L4 chain moved. Clay odds unchanged at ~0.05%.**
